from nodes.file_analysis import analyze_repo_code
from nodes.dependency_sorter import topological_sort
from nodes.git_clone import clone_repo
from nodes.micro_service_identification import generate_microservice_list
from nodes.service_split import generate_microservice_code_plan_threaded
from nodes.generate_report import generate_combined_markdown_from_json
from nodes.insert_data import insert_data
from nodes.check_db import check_db
from langsmith import traceable
from langchain_core.runnables.graph import MermaidDrawMethod

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from fastapi import WebSocket


async def safe_send(socket: WebSocket, id: int, status: str, message: str = ""):
    try:
        await socket.send_json(
            {"step": "update", "data": {"id": id, "status": status, "message": message}}
        )
    except Exception as e:
        print(f"[WebSocket Error] Failed to send message: {e}")

async def error_send(socket: WebSocket, error: str):
    try:
        await socket.send_json({
            "step":"completed",
            "success": False,
            "error": error
        })
    except Exception as e:
        print(f"[WebSocket Error] Failed to send message: {e}")

class ProjectState(TypedDict):
    repo_link: str
    destination: str
    present: bool
    file_analysis: dict
    sorted_files: dict
    micro_services_list: dict
    microservice_output: dict
    result: str
    socket: WebSocket


@traceable
async def check_database(state: ProjectState) -> ProjectState:
    print("Checking database")
    try:
        await safe_send(state["socket"], 1, "processing", "Checking database")
        present, data = await check_db(state["repo_link"])
        if present:
            print("[INFO] Data already exists for this repo. Skipping cloning and analysis.")
            state["present"] = True
            state["result"] = data["result"]
            await safe_send(state["socket"], 1, "completed", "Data already exists")
        else:
            state["present"] = False
            await safe_send(state["socket"], 1, "completed", "Data not found")
            print("[INFO] Data not found in database.")
        print("[INFO] Database check completed successfully.")
    except Exception as e:
        print(f"[ERROR] Database check failed: {e}")
        await error_send(state["socket"], "Database check failed.")
    return state


@traceable
async def clone_repository(state: ProjectState) -> ProjectState:
    try:
        print("Cloning repository")
        await safe_send(state["socket"], 2, "processing", "Cloning repository")
        destination = state["destination"]
        repo_link = state["repo_link"]
        cloned = await clone_repo(repo_link, destination)
        if not cloned:
            print("[ERROR] Repository cloning failed.")
            await error_send(state["socket"], "Repository cloning failed.")
        else:
            await safe_send(state["socket"], 2, "completed", "Repository cloned")
            print("[INFO] Repository cloned successfully.")
    except Exception as e:
        print(f"[ERROR] Repository cloning failed: {e}")
        await error_send(state["socket"], "Repository cloning failed.")
    return state


@traceable
async def analyze_repository(state: ProjectState) -> ProjectState:
    try:
        print("Analyzing repository")
        await safe_send(state["socket"], 3, "processing", "Analyzing repository")
        
        file_analysis = await analyze_repo_code(state["destination"])
        state["file_analysis"] = file_analysis
        
        print("[INFO] Repository analysis completed successfully.")
        
    except Exception as e:
        print(f"[ERROR] Repository analysis failed: {e}")
        await error_send(state["socket"], "Repository analysis failed.")
        
    return state

@traceable
async def sort_files_based_on_dependencies(state: ProjectState) -> ProjectState:
    try:
        print("Topological sorting")
        sorted_files = await topological_sort(state["file_analysis"])
        state["sorted_files"] = sorted_files
        await safe_send(state["socket"], 3, "completed", "Repository analyzed")
    except Exception as e:
        print(f"[ERROR] Topological sorting failed: {e}")
        await error_send(state["socket"], "Topological sorting failed.")
    return state


@traceable
async def generate_microservice_list_graph(state: ProjectState) -> ProjectState:
    try:
        print("Generating microservice list")
        await safe_send(state["socket"], 4, "processing", "Generating microservice list")
        
        micro_services_list = await generate_microservice_list(state["sorted_files"])
        state["micro_services_list"] = micro_services_list
        
        await safe_send(state["socket"], 4, "completed", "Microservice list generated")
        print("[INFO] Microservice list generated successfully.")
        
    except Exception as e:
        print(f"[ERROR] Generating microservice list failed: {e}")
        await error_send(state["socket"], "Generating microservice list failed.")
        
    return state


@traceable
async def generate_microservice_code_plan(state: ProjectState) -> ProjectState:
    try:
        print("Generating microservice code plan")
        await safe_send(state["socket"], 5, "processing", "Generating microservice code plan")
        
        microservice_output = await generate_microservice_code_plan_threaded(
            state["sorted_files"], state["micro_services_list"]
        )
        state["microservice_output"] = microservice_output
        
        await safe_send(state["socket"], 5, "completed", "Microservice code plan generated")
        print("[INFO] Microservice code plan generated successfully.")
        
    except Exception as e:
        print(f"[ERROR] Generating microservice code plan failed: {e}")
        await error_send(state["socket"], "Generating microservice code plan failed.")
        
    return state


@traceable
async def generate_combined_markdown(state: ProjectState) -> ProjectState:
    try:
        print("Generating combined markdown")
        await safe_send(state["socket"], 6, "processing", "Generating combined markdown")
        
        result = await generate_combined_markdown_from_json(state["microservice_output"])
        state["result"] = result
        
        print("[INFO] Combined markdown generated successfully.")
        
    except Exception as e:
        print(f"[ERROR] Generating combined markdown failed: {e}")
        await error_send(state["socket"], "Generating combined markdown failed.")
        
    return state


@traceable
async def insert_data_into_database(state: ProjectState) -> ProjectState:
    try:
        print("Inserting data into database")
        if await insert_data(state["repo_link"], state["result"]):
            print("[SUCCESS] Data inserted successfully.")
        else:
            print("[FAILED] Data insertion failed.")
    except Exception as e:
        print(f"[ERROR] Data insertion failed: {e}")
    await safe_send(state["socket"], 6, "completed", "Combined markdown generated")
    return state


@traceable
async def exists_in_database(state: ProjectState) -> ProjectState:
    print("Check if data exists in database")
    if state["present"]:
        return "Present"
    else:
        return "Not Present"


graph = StateGraph(ProjectState)

graph.add_node("Check Database", check_database)
graph.add_node("Clone Repository", clone_repository)
graph.add_node("Analyse Repository Files", analyze_repository)
graph.add_node(
    "Sort Files based on Internal Dependencies", sort_files_based_on_dependencies
)
graph.add_node("Generate Microservices List", generate_microservice_list_graph)
graph.add_node("Generate Code Plan", generate_microservice_code_plan)
graph.add_node("Generate Combine Markdown", generate_combined_markdown)
graph.add_node("Insert into Database", insert_data_into_database)

graph.add_edge(START, "Check Database")
graph.add_conditional_edges(
    "Check Database",
    exists_in_database,
    {"Not Present": "Clone Repository", "Present": END},
)
graph.add_edge("Clone Repository", "Analyse Repository Files")
graph.add_edge("Analyse Repository Files", "Sort Files based on Internal Dependencies")
graph.add_edge(
    "Sort Files based on Internal Dependencies", "Generate Microservices List"
)
graph.add_edge("Generate Microservices List", "Generate Code Plan")
graph.add_edge("Generate Code Plan", "Generate Combine Markdown")
graph.add_edge("Generate Combine Markdown", "Insert into Database")
graph.add_edge("Insert into Database", END)

app = graph.compile()


async def invoke_graph(repo_url: str, destination: str, socket: WebSocket=None):
    state = ProjectState(
        repo_link=repo_url,
        destination=destination,
        present=False,
        file_analysis={},
        sorted_files={},
        micro_services_list={},
        microservice_output={},
        result="",
        socket=socket,
    )
    final_state = await app.ainvoke(state)
    
    await state["socket"].send_json(
        { "success": True, "downloadContent": final_state["result"]}
    )


# if __name__ == "__main__":

#     img = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

#     with open ("graph.png", "wb") as f:
#         f.write(img)

#     print("Graph image saved as graph.png")
