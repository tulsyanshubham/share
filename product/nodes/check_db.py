# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.database import get_collection

def check_db(repo_link: str):
    REPO_URL = repo_link.split("github.com/")[-1].replace(".git", "").strip()
    collection = get_collection()
    record = collection.find_one({"repo_link": REPO_URL})
    if record:
        return True,{
            "file_split": record["file_split"],
            "folder_structure": record["folder_structure"]
        }
    else:
        return False, None
