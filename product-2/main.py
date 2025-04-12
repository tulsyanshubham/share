from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from graph import invoke_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo_link = ""
socket = None
result = ""

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        repo_url = await websocket.receive_text()
        await websocket.send_text(f"📥 Received repo URL: {repo_url}")

        # 🧠 Call the main function that does your pipeline
        await invoke_graph(repo_url, "./monolith_code", websocket)

        await websocket.send_text("✅ Migration analysis complete.")

    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        await websocket.send_text(f"❌ Error occurred: {str(e)}")