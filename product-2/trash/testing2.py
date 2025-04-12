import os
import json
import time
import chromadb
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from autogen import ConversableAgent

# === Load environment variables ===
load_dotenv()
GROQ_API_KEY = os.getenv("OPEN_AI_API_KEY")



# === Config ===\
GROQ_API_URL = "https://api.openai.com/v1/chat/completions"
GROQ_MODEL = "gpt-4"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 2000

# === SentenceTransformer Embedding Function ===
class LocalEmbeddingFunction(DefaultEmbeddingFunction):
    def _init_(self, model_name=EMBED_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def _call_(self, texts):
        return self.model.encode(texts).tolist()

embedding_func = LocalEmbeddingFunction()

# === Setup ChromaDB ===
client = chromadb.Client()
collection = client.get_or_create_collection("summaries", embedding_function=embedding_func)

# === Use AutoGen Agent to call Groq ===
class GroqAgent(ConversableAgent):
    def summarize(self, content: str) -> str:
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following:\n\n{content}"}
            ],
            "temperature": 0.5,
            "max_tokens": 300
        }
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            raise Exception(f"Groq API Error: {response.status_code} - {response.text}")

agent = GroqAgent(name="groq-agent")

# === Chunking Function ===
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# === Store in Chroma ===
def store_summary(original: str, summary: str, metadata: dict = {}):
    doc_id = str(abs(hash(original)))[:16]
    collection.add(
        documents=[original],
        metadatas=[{"summary": summary, **metadata}],
        ids=[doc_id]
    )
    print(f"\n✅ Stored in ChromaDB with ID: {doc_id}")

# === Query Chroma ===
def query_summary(query: str, top_k: int = 3):
    results = collection.query(query_texts=[query], n_results=top_k)
    print("\n📚 Top Results:\n")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"Document:\n{doc}\nSummary: {meta['summary']}\n---\n")

# === Main Flow ===
def main():
    mode = input("Enter mode (summarize / retrieve): ").strip().lower()

    if mode == "summarize":
        path = input("Enter path to .json file: ").strip()
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
        print(f"\n🔍 JSON split into {len(chunks)} chunks. Generating summaries...\n")
        chunk_summaries = []

        for i, chunk in enumerate(chunks):
            print(f"🧠 Summarizing chunk {i+1}/{len(chunks)}...")
            summary = agent.summarize(chunk)
            chunk_summaries.append(summary)
            time.sleep(0.5)  # Delay to avoid rate limit

        final_input = "\n\n".join([f"Chunk {i+1} Summary: {s}" for i, s in enumerate(chunk_summaries)])
        print("\n📦 Generating final summary from chunk summaries...\n")
        final_summary = agent.summarize(final_input)

        print(f"\n📝 Final Summary:\n{final_summary}")
        store_summary(full_text, final_summary, metadata={"source_file": path})

    elif mode == "retrieve":
        query = input("Enter your search query: ")
        query_summary(query)

    else:
        print("❌ Invalid mode. Choose 'summarize' or 'retrieve'.")

if __name__ == "__main__":
    main()