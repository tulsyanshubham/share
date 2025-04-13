import os
import json
import threading
import openai
from pathlib import Path
from typing import List
from queue import Queue
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

MAX_CHARS = 8000
max_threads = 8

skip_files = (
    'package-info.java', 'module-info.java', 'pom.xml', 'Dockerfile',
    '.gitignore', 'README.md', 'LICENSE', 'Makefile', '.editorconfig',
    '.env', '.dockerignore', '.prettierrc', '.eslintrc', '.babelrc',
    'yarn.lock', 'pnpm-lock.yaml', 'package-lock.json', 'tsconfig.json',
    'Test.java', 'Tests.java'
)
consider_extensions = (
    '.py', '.js', '.ts', '.java', '.go', '.rb', '.cs', '.cpp', '.c',
    '.kt', '.swift', '.rs', '.php'
)

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
            combined_analysis["internal_dependencies"] = list(set(combined_analysis["internal_dependencies"]))
            combined_analysis["external_dependencies"] = list(set(combined_analysis["external_dependencies"]))
            with lock:
                results.append(combined_analysis)
        except Exception as e:
            print(f"[ERROR] Failed analyzing file {file_path}: {e}")
        finally:
            queue.task_done()

async def analyze_repo_code(repo_path: str) -> List[dict]:
    file_queue = Queue()
    results = []
    lock = threading.Lock()
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(consider_extensions) and not file.endswith(skip_files):
                file_queue.put(Path(root) / file)
    threads = []
    for _ in range(min(max_threads, file_queue.qsize())):
        t = threading.Thread(target=worker, args=(file_queue, results, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print(f"[SUCCESS] Analysis completed. Returning {len(results)} results.")
    return results

# if __name__ == "__main__":
#     results = analyze_repo_code("./monolith_code")
#     with open("file_analysis.json", "w") as f:
#         json.dump(results, f, indent=2)