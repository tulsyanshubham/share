import requests
import json
import os
from requests.utils import quote
import threading
from queue import Queue

# output_dir = "output"
# os.makedirs(output_dir, exist_ok=True)

skip_files = {
    ".gitignore", "README.md", "LICENSE", ".dockerignore",
    ".env", ".editorconfig", "package-lock.json", "node_modules"
}
skip_extensions = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".svg",
    ".zip", ".tar", ".gz", ".exe", ".dll", ".so", ".jar",
    ".bin", ".lock", ".mp4", ".mkv", ".mp3", ".m3u8", ".mov",
    ".avi", ".flv", ".webm", ".wav", ".aac", ".ogg", ".opus",
    ".m4a", ".3gp", ".3g2", ".wma", ".doc", ".docx", ".xls",
    ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".csv",
    ".json", ".xml", ".yaml", ".yml", ".html", ".css"
}

def get_default_branch(GITHUB_REPO,HEADERS):
    url = f"https://api.github.com/repos/{GITHUB_REPO}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    return "main"

def get_repo_contents(GITHUB_REPO,HEADERS,path=""):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{quote(path)}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Failed to fetch {url}: {response.status_code}")
        return []
    
def get_file_content(GITHUB_REPO,DEFAULT_BRANCH,file_path):
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{DEFAULT_BRANCH}/{quote(file_path)}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None

def repo_scan(repo_url="https://github.com/tulsyanshubham/TipyDo-Backend.git"):
    GITHUB_REPO = repo_url.split("github.com/")[-1].replace(".git", "").strip()
    GITHUB_TOKEN = os.getenv("GITHUB_PAT")
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

    DEFAULT_BRANCH = get_default_branch(GITHUB_REPO,HEADERS)
    print(f"[INFO] Default branch: {DEFAULT_BRANCH}")

    file_data_lock = threading.Lock()
    dependencies_lock = threading.Lock()

    def analyze_repo(path="", max_threads=8):
        repo_structure = get_repo_contents(GITHUB_REPO,HEADERS,path)
        file_data = []
        dependencies = []

        file_queue = Queue()
        
        def process_file_worker():
            while True:
                item = file_queue.get()
                if item is None:
                    file_queue.task_done()
                    break
                    
                print(f"[INFO] Reading file: {item['path']}")
                name = item["name"]
                ext = "." + name.split(".")[-1] if "." in name else ""

                if name in skip_files or ext.lower() in skip_extensions:
                    file_queue.task_done()
                    continue

                file_content = get_file_content(GITHUB_REPO,DEFAULT_BRANCH,item["path"])

                with file_data_lock:
                    file_data.append({
                        "name": name,
                        "size": item["size"],
                        "html_url": item["html_url"],
                        "path": item["path"],
                        "content": file_content
                    })

                if name in ["package.json", "pom.xml", "requirements.txt"]:
                    with dependencies_lock:
                        dependencies.append(item["path"])
                        
                file_queue.task_done()

        threads = []
        for i in range(max_threads):
            t = threading.Thread(target=process_file_worker)
            t.start()
            threads.append(t)

        for item in repo_structure:
            if item["type"] == "dir":
                sub_file_data, sub_dependencies = analyze_repo(item["path"])
                file_data.extend(sub_file_data)
                dependencies.extend(sub_dependencies)
            elif item["type"] == "file":
                file_queue.put(item)

        file_queue.join()
        
        for i in range(max_threads):
            file_queue.put(None)
        for t in threads:
            t.join()

        return file_data, dependencies

    files, dep_files = analyze_repo()
    dependencies = {file: get_file_content(file) for file in dep_files}

    report = {
        "repo": GITHUB_REPO,
        "total_files": len(files),
        # "largest_files": sorted(files, key=lambda x: x["size"], reverse=True)[:5],
        "files": files,
        "dependencies": dependencies
    }

    # repo_scan_report_path = os.path.join(output_dir, "repo_scan_report.json")
    # with open(repo_scan_report_path, "w") as f:
    #     json.dump(report, f, indent=4)

    print("[INFO] Scan Completed: Report saved as repo_scan_report.json")
    return report

# print(repo_scan())