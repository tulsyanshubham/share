import os
import json
import openai
import re
import threading
from queue import Queue
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def clean_json_output(text):
    return re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.IGNORECASE).strip()

def analyze_file_and_assign(file_obj, microservices):
    print(f"[INFO] Analyzing and splitting {file_obj['file_name']}")
    prompt = f"""
You are an expert software architect helping migrate a monolithic codebase to microservices.

Below is a file's metadata including its functions and dependencies. Based on this, determine:
1. Which microservice(s) this file should belong to (based on the business domain).
2. The new file path and file name inside the microservice.
3. The functions in this file and a brief description of each.
4. If any function calls another microservice, indicate which.

Return a JSON array with the following structure (even if the file belongs to just one service):

[
  {{
    "microservice_name": "CatalogService",
    "file_name": "ProductRepository.java",
    "file_path": "catalog/domain/ProductRepository.java",
    "functions": [
      {{
        "name": "findByCode",
        "description": "Finds a product by code and returns Optional<ProductEntity>",
        "calls_to_other_microservices": []
      }}
    ]
  }}
]

File Metadata:
{json.dumps(file_obj, indent=2)}

Here's the list of available microservices:
{json.dumps(microservices, indent=2)}

Return ONLY valid JSON.
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    result_text = response.choices[0].message.content.strip()
    cleaned = clean_json_output(result_text)
    return json.loads(cleaned)

def worker(queue, microservices, results, lock):
    while True:
        item = queue.get()
        if item is None:
            break
        try:
            output = analyze_file_and_assign(item, microservices)
            with lock:
                results.append((item["file_name"], output))
        except Exception as e:
            print(f"[ERROR] Failed to process {item['file_name']}: {e}")
        queue.task_done()

async def generate_microservice_code_plan_threaded(sorted_files, microservices, num_threads=8):
    queue = Queue()
    results = []
    lock = threading.Lock()

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(queue, microservices, results, lock))
        t.start()
        threads.append(t)

    for file_obj in sorted_files:
        queue.put(file_obj)

    queue.join()

    for _ in threads:
        queue.put(None)
    for t in threads:
        t.join()

    microservice_outputs = {}
    for _, output in results:
        for result in output:
            ms_name = result["microservice_name"]
            key = f"{ms_name}"
            if key not in microservice_outputs:
                microservice_outputs[key] = []

            existing_file = next((f for f in microservice_outputs[key] if f["file_path"] == result["file_path"]), None)
            if existing_file:
                existing_file["functions"].extend(result["functions"])
            else:
                microservice_outputs[key].append(result)

    print(f"[SUCCESS] Processed microservice plan for {len(microservice_outputs)} services")
    return microservice_outputs