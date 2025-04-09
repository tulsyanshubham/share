# import os
import json
import re
# from groq import Groq
# from itertools import cycle
import threading
from queue import Queue
from config.groq import groq_cycle

# apiKeys = [
#     os.environ.get("GROQ_API_KEY_1"),
#     os.environ.get("GROQ_API_KEY_2"),
#     os.environ.get("GROQ_API_KEY_3"),
#     os.environ.get("GROQ_API_KEY_4"),
#     os.environ.get("GROQ_API_KEY_5"),
#     os.environ.get("GROQ_API_KEY_6"),
#     os.environ.get("GROQ_API_KEY_7"),
#     os.environ.get("GROQ_API_KEY_8"),
# ]

# groqClients = [Groq(api_key=key) for key in apiKeys]

# output_dir = "output"
# os.makedirs(output_dir, exist_ok=True)

# repo_scan_report = os.path.join(output_dir, "repo_scan_report.json")
# with open(repo_scan_report, "r") as file:
#     repo_data = json.load(file)

# groq_cycle = cycle(groqClients)


def call_groq(prompt):
    groq = next(groq_cycle)
    chat_completion = groq.chat.completions.create(
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def worker(queue, file_list, microservices, file_descriptions, lock):
    while not queue.empty():
        file = queue.get()
        prompt = f"""
        You are an expert software architect analyzing a monolithic codebase to plan its migration to a microservices architecture. 

        ### Task:
        Determine whether the given file should be split into smaller, more modular files as part of a microservices-based system.
        Make sure to give output in single valid JSON format only.

        ### Given File:
        - **Name**: {file["name"]}
        - **Path**: {file["path"]}
        - **Content**: {file["content"][:2000]}  # Limiting content to prevent exceeding token limits

        ### Project Context:
        Here is a list of all the files in the repository to provide context:
        {json.dumps(file_list)}

        ### Instructions:
        - **Analyze** the given file and decide whether it needs to be split.
        - **If splitting is needed**, generate new file paths and names that describe their intended purpose.
        - **If the file does NOT need to be split**, return the file in the same path.
        - **Additionally**, provide a short description for each new file, explaining its functionality.
        - **Ensure that the output strictly follows the JSON format below**.

        ### Response Format:
        Your response must be in **valid JSON format**, following this structure:
        ```json
        {{
            "microservice_mapping": {{
                "{file["path"]}": ["new_file_path_with_name.py", "new_file_path_with_name.py"]
            }},
            "file_descriptions": {{
                "new_file_path_with_name.py": "Short description of its functionality",
                "new_file_path_with_name.py": "Another short description"
            }}
        }}
        ```

        ### Rules:
        1. **Only split if necessary** : If the file is already modular, return its original path without modifications.
        2. **Maintain file relationships** : If splitting, ensure logically related functions remain together.
        3. **Use meaningful names** : New filenames should clearly reflect their role in the microservices architecture.
        4. **Provide concise descriptions** : Explain the functionality of each new file in one sentence.
        5. **No explanations or extra text** : Only return valid JSON.

        ### Example Responses:

        #### **Case 1: The file needs to be split**
        ```json
        {{
            "microservice_mapping": {{
                "{file["path"]}": ["services/auth/user_auth.py", "services/auth/token_handler.py"]
            }},
            "file_descriptions": {{
                "services/auth/user_auth.py": "Handles user authentication and session management.",
                "services/auth/token_handler.py": "Manages JWT token generation and validation."
            }}
        }}
        ```

        #### **Case 2: The file does NOT need to be split**
        ```json
        {{
            "microservice_mapping": {{
                "{file["path"]}": ["{file["path"]}"]
            }},
            "file_descriptions": {{
                "{file["path"]}": "This file does not need splitting and remains unchanged."
            }}
        }}
        ```

        Now, analyze the given file and generate the response in the requested format.
        """

        try:
            print(f"[INFO] Processing file: {file['name']}")
            json_output = call_groq(prompt)

            json_match = re.search(r"\{.*\}", json_output, re.DOTALL)
            if not json_match:
                raise ValueError("No valid JSON found in the response.")

            json_str = json_match.group(0)
            response_data = json.loads(json_str)

            with lock:
                microservices.update(response_data.get("microservice_mapping", {}))
                file_descriptions.update(response_data.get("file_descriptions", {}))

        except Exception as e:
            print(f"[ERROR] Failed to process {file['name']}: {e}")
        finally:
            queue.task_done()

def determine_microservice_splits(repo_data, num_threads=5):
    file_list = [file["name"] for file in repo_data["files"]]
    microservices = {}
    file_descriptions = {}

    q = Queue()
    lock = threading.Lock()

    for file in repo_data["files"]:
        q.put(file)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q, file_list, microservices, file_descriptions, lock))
        t.start()
        threads.append(t)

    q.join()

    for t in threads:
        t.join()

    return microservices, file_descriptions

def file_split(repo_data):
    print("[INFO] Determining microservice splits...")
    microservices, file_descriptions = determine_microservice_splits(repo_data)

    nested_output = {}
    for js_file, py_files in microservices.items():
        nested_output[js_file] = {
            py_file: file_descriptions[py_file] for py_file in py_files
        }

    # microservices_path = os.path.join(output_dir, "microservice_splits.json")
    # file_descriptions_path = os.path.join(output_dir, "file_descriptions.json")
    # file_combined = os.path.join(output_dir, "file_combined.json")

    # with open(microservices_path, "w") as outfile:
    #     json.dump(microservices, outfile, indent=4)

    # with open(file_descriptions_path, "w") as outfile:
    #     json.dump(file_descriptions, outfile, indent=4)

    # with open(file_combined, "w") as outfile:
    #     json.dump(nested_output, outfile, indent=4)
    return microservices, file_descriptions, nested_output