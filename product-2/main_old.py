from nodes.file_analysis import analyze_repo_code
from nodes.dependency_sorter import topological_sort
from nodes.git_clone import clone_repo
from nodes.micro_service_identification import generate_microservice_list
from nodes.service_split import generate_microservice_code_plan_threaded
from nodes.generate_report import generate_combined_markdown_from_json
from nodes.insert_data import insert_data
from nodes.check_db import check_db

def main(repo_url,):
    destination = "./monolith_code"
    present, data = check_db(repo_url)
    if present:
        print("[INFO] Data already exists for this repo. Skipping cloning and analysis.")
        return data["result"]
    
    clone_repo(repo_url, destination)
    file_analysis = analyze_repo_code("./monolith_code")
    sorted_files = topological_sort(file_analysis)
    micro_services_list = generate_microservice_list(sorted_files)
    microservice_output = generate_microservice_code_plan_threaded(sorted_files, micro_services_list)
    result = generate_combined_markdown_from_json(microservice_output)
    
    if (insert_data(repo_url,result)):
        print("[SUCCESS] Data inserted successfully.")
    else:
        print("[FAILED] Data insertion failed.")
    return result
        
        
if __name__ == "__main__":
    result = main("https://github.com/oiraqi/xcommerce-monolithic.git")
    with (open("migration_summary.md", "w", encoding="utf-8")) as f:
        f.write(result)