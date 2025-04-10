import os
import json
import chromadb
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from autogen import ConversableAgent

# === Load environment variables ===
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_AI_API_KEY")

# === Config ===
OPEN_API_URL = "https://api.openai.com/v1/chat/completions"
GROQ_MODEL = "gpt-4"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 18000  # characters per chunk

# === SentenceTransformer Embedding Function ===
class LocalEmbeddingFunction(DefaultEmbeddingFunction):
    def __init__(self, model_name=EMBED_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def __call__(self, texts):
        return self.model.encode(texts).tolist()

embedding_func = LocalEmbeddingFunction()

# === Setup ChromaDB ===
client = chromadb.Client()
collection = client.get_or_create_collection("microservices", embedding_function=embedding_func)

# === Use AutoGen Agent to call Groq ===
class GroqAgent(ConversableAgent):
        def generate_microservices(self, content: str) -> dict:
            payload = {
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a software architect helping to migrate a monolith to microservices. "
                            "Given code and analysis, return a JSON object describing a single microservice. "
                            "Use the following format:\n\n"
                            "{\n"
                            "  \"microservice_name\": \"...\",\n"
                            "  \"description\": \"...\",\n"
                            "  \"related_files\": [\"...\"],\n"
                            "  \"dependencies\": [\"...\"]\n"
                            "}\n"
                            "Make sure the response is valid JSON."
                        )
                    },
                    {"role": "user", "content": content}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            headers = {
                "Authorization": f"Bearer {OPEN_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(OPEN_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                response_text = response.json()["choices"][0]["message"]["content"].strip()
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError as e:
                    print("⚠️ Failed to parse response as JSON:")
                    print(response_text)
                    raise e
            else:
                raise Exception(f"Groq API Error: {response.status_code} - {response.text}")


agent = GroqAgent(name="microservice-agent")

# === Chunking Function ===
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# === Store in ChromaDB ===
def store_microservice_mapping(original: str, mapping: str, metadata: dict = {}):
    doc_id = str(abs(hash(original)))[:16]
    collection.add(
        documents=[original],
        metadatas=[{"microservice_mapping": mapping, **metadata}],
        ids=[doc_id]
    )
    print(f"\n✅ Stored microservice mapping in ChromaDB with ID: {doc_id}")

# === Query ChromaDB ===
def query_microservices(query: str, top_k: int = 3):
    results = collection.query(query_texts=[query], n_results=top_k)
    print("\n🔍 Top Microservice Mapping Results:\n")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"Document Snippet:\n{doc[:300]}...\nMapping: {meta['microservice_mapping']}\n---\n")

# === Main Flow for Step 3 ===
def main():
    mode = input("Enter mode (generate / retrieve): ").strip().lower()

    if mode == "generate":
        path = input("Enter path to .json file (file analysis): ").strip()
        if not os.path.isfile(path) or not path.endswith(".json"):
            print("❌ Invalid file path.")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                full_text = json.dumps(data, indent=2)
        except Exception as e:
            print(f"❌ Error reading JSON: {e}")
            return

        chunks = chunk_text(full_text)
        print(f"\n📦 File analysis split into {len(chunks)} chunks. Generating microservice mappings...\n")
        microservice_mappings = []

        for i, chunk in enumerate(chunks):
            print(f"🔧 Processing chunk {i+1}/{len(chunks)}...")
            mapping = agent.generate_microservices(chunk)
            microservice_mappings.append(mapping)

        all_mappings_text = "\n\n".join([f"Chunk {i+1} Mapping: {m}" for i, m in enumerate(microservice_mappings)])
        print("\n📦 Generating final microservice organization...\n")
        final_mapping = agent.generate_microservices(all_mappings_text)

        print("\n🧭 Final Microservice Architecture:")
        print(json.dumps(final_mapping, indent=2))
        store_microservice_mapping(full_text, json.dumps(final_mapping), metadata={"source_file": path})


    elif mode == "retrieve":
        query = input("Enter your search query (e.g., 'order service'): ")
        query_microservices(query)

    else:
        print("❌ Invalid mode. Choose 'generate' or 'retrieve'.")

if __name__ == "__main__":
    main()
