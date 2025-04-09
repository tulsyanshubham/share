import os
import json
# import re
# from groq import Groq
# from itertools import cycle
from config.groq import groq_cycle
from config.clean_code import clean_code

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

output_dir = "output"
# groqClients = [Groq(api_key=key) for key in apiKeys]

# groq_cycle = cycle(groqClients)


def call_groq(prompt):
    groq = next(groq_cycle)
    chat_completion = groq.chat.completions.create(
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# with open(os.path.join(output_dir, "microservice_splits.json"), "r") as f:
#     microservices = json.load(f)

# with open(os.path.join(output_dir, "file_descriptions.json"), "r") as f:
#     file_descriptions = json.load(f)
#     described_files = list(file_descriptions.keys())

def get_prompt(microservices,described_files):
    return f"""
    You are an expert software architect.

    Based on the following information:
    1. Microservice splits for each original file:
    {json.dumps(microservices, indent=2)}

    2. List of all newly generated files after splitting:
    {json.dumps(described_files, indent=2)}

    Your task is to generate a **clean, organized folder and file structure** for a microservices-based architecture.

    ### Rules:
    - Use **only the filenames** from the list of newly generated files.
    - Use folders **only if the file paths suggest them clearly**, or if multiple files belong to a common module (e.g., `auth`, `db`, `utils`, etc.).
    - If a file does not belong to a group, place it at the root level.
    - Do **not** create new folders unless they are already implied in the file path or there's a clear grouping need.
    - Output must be a tree structure using the following format.
    - No additional text, no comments, no blank lines.

    ### Output Format (Markdown):
    ```
    folder_name
    └── file_name.py
    standalone_file.py
    ```

    **Strictly follow the output format. Use exact file names and folder hints from the paths above.**
    """

def folder_structure(microservices,file_descriptions):
    described_files = list(file_descriptions.keys())
    new_structure = call_groq(get_prompt(microservices,described_files))

    # output_path = os.path.join(output_dir, "new_microservice_structure.txt")
    new_structure = clean_code(new_structure)
    # with open(output_path, "w", encoding="utf-8") as f:
    #     f.write(new_structure)
    print(f"[INFO] New microservices structure saved")
    return new_structure