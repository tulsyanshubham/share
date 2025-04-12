import os
import json
import threading
from queue import Queue
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")

NUM_WORKER_THREADS = 8

def analyze_microservice_data(ms_name, data):
    print("[INFO] Analyzing microservice data for " + ms_name)
    prompt = f"""
    You are a software migration expert. You are analyzing the structure of a microservice based on the following JSON data.

    Generate a clear and well-structured Markdown report with:
    - Microservice name
    - Overview
    - List of files with:
    - **step by step on how to migrate from monolith to microservices architecture for that microservice**
    - make use of diagrams and flowcharts to explain the process
    - File path
    - File purpose with as much detail as possible
    - List of functions with names and descriptions
    - **If any function calls another microservice, mention it clearly.**
    - Use headings, bullet points, and code formatting where appropriate
    - If relevant, add a simple text-based flowchart or dependency hierarchy.

    Here's the input JSON:

    ```json
    {json.dumps(data, indent=2)}
    ```
    Return only the markdown content.
    """ 
    response = openai.chat.completions.create( model="gpt-4", messages=[{"role": "user", "content": prompt}], temperature=0.3 )
    return response.choices[0].message.content.strip()

def worker(queue, results):
    while True: 
        item = queue.get() 
        if item is None: 
            break 
        ms_name, ms_data = item 
        try: 
            md_content = analyze_microservice_data(ms_name, ms_data) 
            results.append(md_content) 
        except Exception as e: 
            print(f"[ERROR] Failed to process {ms_name}: {e}") 
        finally: 
            queue.task_done()

def generate_combined_markdown_from_json(microservice_outputs): 
    print(f"[INFO] Processing {len(microservice_outputs)} microservices.")

    q = Queue()
    results = []
    threads = []

    for _ in range(NUM_WORKER_THREADS):
        t = threading.Thread(target=worker, args=(q, results))
        t.start()
        threads.append(t)

    for ms_name, ms_data in microservice_outputs.items():
        q.put((ms_name, ms_data))

    q.join()

    for _ in range(NUM_WORKER_THREADS):
        q.put(None)
    for t in threads:
        t.join()

    combined_md = "# Microservice Migration Summary\n\n"
    for md in results:
        combined_md += md + "\n\n---\n\n"

    print(f"[SUCCESS] Markdown report generated in-memory.")
    return combined_md