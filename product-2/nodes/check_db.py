from config.database import get_collection

async def check_db(repo_link: str):
    REPO_URL = repo_link.split("github.com/")[-1].replace(".git", "").strip()
    collection = get_collection()
    record = collection.find_one({"repo_link": REPO_URL})
    if record:
        return True,{
            "result": record["result"]
        }
    else:
        return False, None