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

from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class ProjectState(TypedDict):
    repo_link: str
    destination: str
    present: bool
    file_analysis: dict
    sorted_files: dict
    micro_services_list: dict
    microservice_output: dict
    result: str
    socket: any

@traceable
def check_database(state : ProjectState) -> ProjectState:
    print("Checking database")
    present, data = check_db(state["repo_link"])
    if present:
        print("[INFO] Data already exists for this repo. Skipping cloning and analysis.")
        state["present"] = True
        state["result"] = data["result"]
    else:
        state["present"] = False
    return state

@traceable
def clone_repository(state : ProjectState) -> ProjectState:
    print("Cloning repository")
    destination = state["destination"]
    repo_link = state["repo_link"]
    clone_repo(repo_link, destination)
    return state

@traceable
def analyze_repository(state : ProjectState) -> ProjectState:
    print("Analyzing repository")
    file_analysis = analyze_repo_code(state["destination"])
    state["file_analysis"] = file_analysis
    return state

@traceable
def sort_files_based_on_dependencies(state : ProjectState) -> ProjectState:
    print("Topological sorting")
    sorted_files = topological_sort(state["file_analysis"])
    state["sorted_files"] = sorted_files
    return state

@traceable
def generate_microservice_list_graph(state : ProjectState) -> ProjectState:
    print("Generating microservice list")
    micro_services_list = generate_microservice_list(state["sorted_files"])
    state["micro_services_list"] = micro_services_list
    return state

@traceable
def generate_microservice_code_plan(state : ProjectState) -> ProjectState:
    print("Generating microservice code plan")
    microservice_output = generate_microservice_code_plan_threaded(state["sorted_files"], state["micro_services_list"])
    state["microservice_output"] = microservice_output
    return state

@traceable
def generate_combined_markdown(state : ProjectState) -> ProjectState:
    print("Generating combined markdown")
    result = generate_combined_markdown_from_json(state["microservice_output"])
    state["result"] = result
    return state

@traceable
def insert_data_into_database(state : ProjectState) -> ProjectState:
    print("Inserting data into database")
    if insert_data(state["repo_link"], state["result"]):
        print("[SUCCESS] Data inserted successfully.")
    else:
        print("[FAILED] Data insertion failed.")
    return state

@traceable
def exists_in_database(state : ProjectState) -> ProjectState:
    print("Check for errors in the project files")
    if state["present"]:
        return "Present"
    else:
        return "Not Present"

graph = StateGraph(ProjectState)

graph.add_node("Check Database" , check_database)
graph.add_node("Clone Repository" , clone_repository)
graph.add_node("Analyse Repository Files" , analyze_repository)
graph.add_node("Sort Files based on Internal Dependencies" , sort_files_based_on_dependencies)
graph.add_node("Generate Microservices List" , generate_microservice_list_graph)
graph.add_node("Generate Code Plan" , generate_microservice_code_plan)
graph.add_node("Generate Combine Markdown" , generate_combined_markdown)
graph.add_node("Insert into Database" , insert_data_into_database)

graph.add_edge(START,"Check Database")
graph.add_conditional_edges(
    "Check Database",
    exists_in_database,
    {
        "Not Present": "Clone Repository",
        "Present": END
    }
)
graph.add_edge("Clone Repository","Analyse Repository Files")
graph.add_edge("Analyse Repository Files","Sort Files based on Internal Dependencies")
graph.add_edge("Sort Files based on Internal Dependencies","Generate Microservices List")
graph.add_edge("Generate Microservices List","Generate Code Plan")
graph.add_edge("Generate Code Plan","Generate Combine Markdown")
graph.add_edge("Generate Combine Markdown","Insert into Database")
graph.add_edge("Insert into Database",END)

app = graph.compile()

def invoke_graph(repo_url: str, destination: str):
    state = ProjectState(
        repo_link=repo_url,
        destination=destination,
        present=False,
        file_analysis={},
        sorted_files={},
        micro_services_list={},
        microservice_output={},
        result=""
    )
    final_state = app.invoke(state)
    return final_state["result"]

# if __name__ == "__main__":
    
#     img = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    
#     with open ("graph.png", "wb") as f:
#         f.write(img)

#     print("Graph image saved as graph.png")