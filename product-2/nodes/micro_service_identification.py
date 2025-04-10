import json
import os
import openai
import re

openai.api_key = os.environ.get("OPEN_AI_API_KEY")

def clean_json_output(text):
    return re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.IGNORECASE).strip()

def chunk_json_objects(json_list, max_chars=12000):
    chunks = []
    current = []
    total = 0

    for item in json_list:
        item_str = json.dumps(item)
        if total + len(item_str) > max_chars:
            chunks.append(current)
            current = [item]
            total = len(item_str)
        else:
            current.append(item)
            total += len(item_str)

    if current:
        chunks.append(current)
    return chunks

def get_microservices_from_chunk(chunk_data):
    prompt = f"""
    You are a software architecture assistant. Based on the following file analysis,
    your task is to group related files into a limited number of business-focused microservices.

    ✅ STRICT REQUIREMENTS:
    - Return ONLY between **4 and 9 microservices**.
    - If you identify more than 9 logical groupings, COMBINE the most closely related ones.
    - DO NOT exceed 9 microservices under any circumstance.
    - Each microservice should serve a broad business function.
    - Grouping should favor simplicity, cohesion, and real-world service boundaries.

    📦 Output format:
    [
    {{
        "microservice_name": "OrderService",
        "description": "Handles all order-related logic and workflows.",
        "related_files": ["order_handler.py", "order_utils.py"]
    }},
    ...
    ]

    📄 Input Data:
    {json.dumps(chunk_data, indent=2)}

    Return ONLY the JSON array — no extra explanations or formatting.
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result_text = response.choices[0].message.content.strip()

    if not result_text.startswith("["):
        print(f"[WARN] GPT returned unexpected format:\n{result_text}\n")

    return result_text

def merge_microservices_with_llm(microservices, target_min=4, target_max=9):
    if len(microservices) <= target_max:
        return microservices

    prompt = f"""
    You are a senior software architect. You have a list of microservices, but there are too many.
    Your task is to intelligently merge them based on their business domains and purpose.

    📌 REQUIREMENTS:
    - Reduce the list to between {target_min} and {target_max} microservices.
    - Merge closely related microservices based on purpose, description, or overlapping file names.
    - Each merged microservice should still be logically cohesive and serve a clear business function.
    - Combine and deduplicate the related_files lists where necessary.

    📄 Microservices to merge:
    {json.dumps(microservices, indent=2)}

    Return ONLY the final list in this format:
    [
    {{
    "microservice_name": "MergedService",
    "description": "Combines responsibilities of ...",
    "related_files": ["file1.py", "file2.py"]
    }},
    ...
    ]
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result_text = response.choices[0].message.content.strip()
    cleaned = clean_json_output(result_text)
    try:
        merged_microservices = json.loads(cleaned)
        return merged_microservices
    except Exception as e:
        print(f"[ERROR] Failed to parse LLM merge output: {e}")
        return microservices  # Fallback if LLM output breaks

def generate_microservice_list(input_json_path: str, output_json_path: str):
    with open(input_json_path, 'r') as f:
        analysis_data = json.load(f)

    all_chunks = chunk_json_objects(analysis_data)
    all_microservices = []

    print(f"[INFO] Processing {len(all_chunks)} chunks...")

    for i, chunk in enumerate(all_chunks):
        try:
            print(f"[INFO] Analyzing chunk {i+1}/{len(all_chunks)}")
            result_json = get_microservices_from_chunk(chunk)
            cleaned = clean_json_output(result_json)
            microservices = json.loads(cleaned)
            all_microservices.extend(microservices)
        except Exception as e:
            print(f"[ERROR] Failed on chunk {i+1}: {e}")

    if len(all_microservices) > 9:
        print(f"[INFO] Merging {len(all_microservices)} microservices to stay within 4–9...")
        final_microservices = merge_microservices_with_llm(all_microservices, target_min=4, target_max=9)
    else:
        final_microservices = all_microservices

    with open(output_json_path, 'w') as out_f:
        json.dump(final_microservices, out_f, indent=2)

    print(f"[SUCCESS] Microservice list saved to {output_json_path} with {len(final_microservices)} services")

# Example usage
if __name__ == "__main__":
    generate_microservice_list("file_analysis.json", "microservices_list.json")
