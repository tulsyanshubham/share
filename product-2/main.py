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

initial_socket_response = {
    'steps':'init',
    "data" : [{
        "id": 1,
        "title": "Check Database",
        "description": "Checking if data already exists.",
    },
    {
        "id": 2,
        "title": "Clone Repository",
        "description": "Cloning the repository.",
    },
    {
        "id": 3,
        "title": "Analyze Repository Files",
        "description": "Analyzing the files in the repository.",
    },
    {
        "id": 4,
        "title": "Generate Possible Microservices",
        "description": "Generating a list of microservices.",
    },
    {
        "id": 5,
        "title": "Generate Code Plan",
        "description": "Generating a code plan for the microservices.",
    },
    {
        "id": 6,
        "title": "Generate Combined Plan",
        "description": "Generating a combined markdown report.",
    }
]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json(initial_socket_response)
        repo_url = await websocket.receive_text()

        # 🧠 Call the main function that does your pipeline
        if repo_url:
            # 🧠 Start pipeline only after getting a repo URL
            await invoke_graph(repo_url, "./monolith_code", websocket)

            await websocket.send_json({"msg": "✅ Migration analysis complete."})
        else:
            await websocket.send_json({"msg": "❌ No repo URL received."})
        await websocket.close()

    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        await websocket.send_json({"msg": f"❌ Error occurred: {str(e)}"})