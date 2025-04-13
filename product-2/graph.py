from nodes.file_analysis import analyze_repo_code
from nodes.dependency_sorter import topological_sort
from nodes.git_clone import clone_repo
from nodes.micro_service_identification import generate_microservice_list
from nodes.service_split import generate_microservice_code_plan_threaded
from nodes.generate_report import generate_combined_markdown_from_json
from nodes.insert_data import insert_data
from nodes.check_db import check_db
from langsmith import traceable
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from fastapi import WebSocket
# from langchain_core.runnables.graph import MermaidDrawMethod

async def safe_send(socket: WebSocket, id: int, status: str, message: str = ""):
    """Sends an 'update' message via WebSocket."""
    try:
        payload = {
            "type": "update",
            "data": {
                "id": id,
                "status": status,
                "message": message,
            },
        }
        await socket.send_json(payload)
        print(
            f"[WebSocket SENT] Type: update, ID: {id}, Status: {status}, Message: {message}"
        )
    except Exception as e:
        print(f"[WebSocket Error] Failed to send 'update' message: {e}")

async def error_send(socket: WebSocket, error_message: str):
    """Sends a 'finished' message with error status via WebSocket."""
    try:
        payload = {
            "type": "finished",
            "data": {"status": "error", "message": error_message},
        }
        await socket.send_json(payload)
        print(
            f"[WebSocket SENT] Type: finished, Status: error, Message: {error_message}"
        )
    except Exception as e:
        print(f"[WebSocket Error] Failed to send 'finished' error message: {e}")

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
    error_occurred: bool

@traceable
async def check_database(state: ProjectState) -> ProjectState:
    print("--- Node: Check Database ---")
    socket = state["socket"]
    step_id = 1
    try:
        await safe_send(
            socket, step_id, "processing", "Checking database for existing analysis..."
        )
        present, data = await check_db(state["repo_link"])
        if present:
            print("[INFO] Data already exists for this repo. Skipping processing.")
            state["present"] = True
            state["result"] = data[
                "result"
            ]  
            await safe_send(
                socket, step_id, "completed", "Found existing analysis in database."
            )
        else:
            state["present"] = False
            await safe_send(socket, step_id, "completed", "No existing analysis found.")
            print("[INFO] Data not found in database.")
        print("[INFO] Database check completed.")
    except Exception as e:
        print(f"[ERROR] Database check failed: {e}")
        await error_send(socket, f"Database check failed: {str(e)}")
        state["error_occurred"] = True  
    return state

@traceable
async def clone_repository(state: ProjectState) -> ProjectState:
    print("--- Node: Clone Repository ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 2
    try:
        print("Cloning repository")
        await safe_send(
            socket, step_id, "processing", f"Cloning repository: {state['repo_link']}"
        )
        destination = state["destination"]
        repo_link = state["repo_link"]
        cloned = await clone_repo(repo_link, destination)
        if not cloned:
            print("[ERROR] Repository cloning failed.")
            await error_send(
                socket, "Repository cloning failed. Check URL and permissions."
            )
            state["error_occurred"] = True  
        else:
            await safe_send(
                socket, step_id, "completed", "Repository cloned successfully."
            )
            print("[INFO] Repository cloned successfully.")
    except Exception as e:
        print(f"[ERROR] Repository cloning failed: {e}")
        await error_send(socket, f"Repository cloning failed: {str(e)}")
        state["error_occurred"] = True  
    return state


@traceable
async def analyze_repository(state: ProjectState) -> ProjectState:
    print("--- Node: Analyze Repository ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 3  
    try:
        print("Analyzing repository")
        
        await safe_send(
            socket,
            step_id,
            "processing",
            "Analyzing code structure and dependencies...",
        )
        file_analysis = await analyze_repo_code(state["destination"])
        state["file_analysis"] = file_analysis
        print("[INFO] Repository analysis part completed.")
        
    except Exception as e:
        print(f"[ERROR] Repository analysis failed: {e}")
        await error_send(socket, f"Repository analysis failed: {str(e)}")
        await safe_send(
            socket, step_id, "error", "Analysis failed."
        )  
        state["error_occurred"] = True  
    return state

@traceable
async def sort_files_based_on_dependencies(state: ProjectState) -> ProjectState:
    print("--- Node: Sort Files ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 3  
    try:
        print("Topological sorting")     
        sorted_files = await topological_sort(state["file_analysis"])
        state["sorted_files"] = sorted_files
        print("[INFO] Topological sorting completed.")
        
        await safe_send(
            socket,
            step_id,
            "completed",
            "Code analysis and dependency sorting complete.",
        )
    except Exception as e:
        print(f"[ERROR] Topological sorting failed: {e}")
        await error_send(socket, f"Topological sorting failed: {str(e)}")
        await safe_send(
            socket, step_id, "error", "Dependency sorting failed."
        )  
        state["error_occurred"] = True  
    return state

@traceable
async def generate_microservice_list_graph(state: ProjectState) -> ProjectState:
    print("--- Node: Generate Microservice List ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 4
    try:
        print("Generating microservice list")
        await safe_send(
            socket,
            step_id,
            "processing",
            "Identifying potential microservice boundaries...",
        )
        micro_services_list = await generate_microservice_list(state["sorted_files"])
        state["micro_services_list"] = micro_services_list
        await safe_send(
            socket, step_id, "completed", "Potential microservices identified."
        )
        print("[INFO] Microservice list generated successfully.")
    except Exception as e:
        print(f"[ERROR] Generating microservice list failed: {e}")
        await error_send(socket, f"Generating microservice list failed: {str(e)}")
        await safe_send(
            socket, step_id, "error", "Failed to identify microservices."
        )  
        state["error_occurred"] = True  
    return state


@traceable
async def generate_microservice_code_plan(state: ProjectState) -> ProjectState:
    print("--- Node: Generate Code Plan ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 5
    try:
        print("Generating microservice code plan")
        await safe_send(
            socket,
            step_id,
            "processing",
            "Mapping files and functions to microservices...",
        )
        microservice_output = await generate_microservice_code_plan_threaded(
            state["sorted_files"], state["micro_services_list"]
        )
        state["microservice_output"] = microservice_output
        await safe_send(
            socket, step_id, "completed", "Code plan for microservices generated."
        )
        print("[INFO] Microservice code plan generated successfully.")
    except Exception as e:
        print(f"[ERROR] Generating microservice code plan failed: {e}")
        await error_send(socket, f"Generating microservice code plan failed: {str(e)}")
        await safe_send(
            socket, step_id, "error", "Failed to generate code plan."
        )  
        state["error_occurred"] = True  
    return state


@traceable
async def generate_combined_markdown(state: ProjectState) -> ProjectState:
    print("--- Node: Generate Combined Markdown ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 6
    try:
        print("Generating combined markdown report")
        await safe_send(
            socket, step_id, "processing", "Compiling the final migration report..."
        )
        result = await generate_combined_markdown_from_json(
            state["microservice_output"]
        )
        state["result"] = result
        
        print("[INFO] Combined markdown generated successfully.")
    except Exception as e:
        print(f"[ERROR] Generating combined markdown failed: {e}")
        await error_send(
            socket, f"Generating combined markdown report failed: {str(e)}"
        )
        await safe_send(
            socket, step_id, "error", "Failed to generate report."
        )  
        state["error_occurred"] = True  
    return state

@traceable
async def insert_data_into_database(state: ProjectState) -> ProjectState:
    print("--- Node: Insert into Database ---")
    if state.get("error_occurred"):
        return state  
    socket = state["socket"]
    step_id = 6  
    try:
        print("Inserting data into database")
        if await insert_data(state["repo_link"], state["result"]):
            print("[SUCCESS] Data inserted/updated successfully.")
            await safe_send(
                socket, step_id, "completed", "Migration report generated and saved."
            )
        else:
            
            print("[WARNING] Data insertion/update failed. Report still generated.")
            
            await safe_send(
                socket,
                step_id,
                "completed",
                "Migration report generated (database save failed).",
            )
    except Exception as e:
        
        print(f"[ERROR] Data insertion failed: {e}")
        
        await safe_send(
            socket,
            step_id,
            "completed",
            f"Migration report generated (database save error: {e}).",
        )
    return state

@traceable
async def should_process_repo(state: ProjectState) -> str:
    print("--- Edge: Check DB Result ---")
    if state.get("error_occurred"):
        print("[INFO] Error occurred in Check DB, stopping.")
        return END  
    if state["present"]:
        print("[INFO] Data found in DB. Path: Present")
        return "Present"  
    else:
        print("[INFO] Data not found in DB. Path: Not Present")
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
    should_process_repo,
    {
        "Not Present": "Clone Repository",  
        "Present": END,  
        END: END,  
    },
)

graph.add_edge("Clone Repository", "Analyse Repository Files")
graph.add_edge("Analyse Repository Files", "Sort Files based on Internal Dependencies")
graph.add_edge("Sort Files based on Internal Dependencies", "Generate Microservices List")
graph.add_edge("Generate Microservices List", "Generate Code Plan")
graph.add_edge("Generate Code Plan", "Generate Combine Markdown")
graph.add_edge("Generate Combine Markdown", "Insert into Database")
graph.add_edge("Insert into Database", END)

app = graph.compile()

async def invoke_graph(repo_url: str, destination: str, socket: WebSocket):
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
        error_occurred=False,  
    )
    final_state = None
    try:
        print("\nInvoking LangGraph execution...")
        final_state = await app.ainvoke(state)
        print("LangGraph execution finished.")
        
        if final_state.get("error_occurred"):
            print(
                "[INFO] Graph finished, but an error occurred previously. No success message sent."
            )
            
            return
        
        if final_state and final_state.get("result"):
            print("[INFO] Sending final 'finished' success message.")
            await socket.send_json(
                {
                    "type": "finished",
                    "data": {
                        "status": "completed",
                        "message": final_state["result"],  
                    },
                }
            )
            print("[WebSocket SENT] Type: finished, Status: completed")
        else:
            print("[WARNING] Graph finished but no result found in final state.")
            await error_send(
                socket, "Processing finished, but no result was generated."
            )
    except Exception as e:
        print(f"[CRITICAL ERROR] Error invoking graph: {e}")
        if final_state and not final_state.get("error_occurred"):
            await error_send(
                socket, f"An unexpected error occurred during processing: {str(e)}"
            )

# if __name__ == "__main__":
    
#     img = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    
#     with open ("graph.png", "wb") as f:
#         f.write(img)

#     print("Graph image saved as graph.png")