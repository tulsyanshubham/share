import os
import json
import threading
import openai
from pathlib import Path
from typing import List
from queue import Queue

openai.api_key = os.environ.get("OPEN_AI_API_KEY")

MAX_CHARS = 8000
max_threads = 8
skip_files = ('package-info.java', 'module-info.java', 'pom.xml', 'Dockerfile', '.gitignore', 'README.md', '.git', "Test.java", "Tests.java")

def read_code_file(file_path: Path) -> List[str]:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    return [code[i:i + MAX_CHARS] for i in range(0, len(code), MAX_CHARS)]

def analyze_chunk(chunk: str, file_name: str) -> str:
    prompt = f"""
        You are a software architect assistant. Analyze the following code chunk from a file named '{file_name}'.
        Return a JSON object with the following fields:
        - "internal_dependencies": list of filenames this code depends on
        - "external_dependencies": list of libraries or packages it uses
        - "functions": an array of descriptions of the functions in this code as well as the name of internal dependencies they use (if any).

        Code:
        ```
        {chunk}
        ```

        Only return the JSON, nothing else.
        """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def worker(queue: Queue, results: List[dict], lock: threading.Lock):
    while not queue.empty():
        file_path = queue.get()
        file = file_path.name

        print(f"[INFO] Analyzing {file_path}")
        try:
            file_chunks = read_code_file(file_path)
            combined_analysis = {
                "file_name": file,
                "file_path": str(file_path),
                "internal_dependencies": [],
                "external_dependencies": [],
                "functions": []
            }

            for chunk in file_chunks:
                try:
                    analysis = analyze_chunk(chunk, file)
                    data = json.loads(analysis)
                    combined_analysis["internal_dependencies"].extend(data.get("internal_dependencies", []))
                    combined_analysis["external_dependencies"].extend(data.get("external_dependencies", []))
                    combined_analysis["functions"].extend(data.get("functions", []))
                except Exception as e:
                    print(f"[ERROR] Failed analyzing chunk from {file}: {e}")

            # Remove duplicates
            combined_analysis["internal_dependencies"] = list(set(combined_analysis["internal_dependencies"]))
            combined_analysis["external_dependencies"] = list(set(combined_analysis["external_dependencies"]))

            with lock:
                results.append(combined_analysis)

        except Exception as e:
            print(f"[ERROR] Failed analyzing file {file_path}: {e}")
        finally:
            queue.task_done()

def analyze_repo_code(repo_path: str, output_json_path: str):
    file_queue = Queue()
    results = []
    lock = threading.Lock()

    # Populate queue with all valid code files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.java', '.go', '.rb')) and not file.endswith(skip_files):
                file_queue.put(Path(root) / file)

    # Start worker threads
    threads = []
    for _ in range(min(max_threads, file_queue.qsize())):
        t = threading.Thread(target=worker, args=(file_queue, results, lock))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Save output
    with open(output_json_path, 'w') as out_f:
        json.dump(results, out_f, indent=2)
    print(f"[SUCCESS] Analysis saved to {output_json_path}")

# Example usage
if __name__ == "__main__":
    analyze_repo_code("./monolith_code", "file_analysis.json")