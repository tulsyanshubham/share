from config.schema import MigrationSchema
from config.database import get_collection
from pydantic import ValidationError

def upsert_migration(data: dict):
    try:
        validated = MigrationSchema(**data)
        collection = get_collection()

        result = collection.update_one(
            {"repo_link": validated.repo_link},
            {"$set": validated.model_dump()},
            upsert=True
        )

        if result.upserted_id:
            print("[✅] Data inserted successfully.")
        elif result.modified_count > 0:
            print("[✅] Existing data updated successfully.")
        else:
            print("[ℹ️] No changes made (data may already be up to date).")

    except ValidationError as e:
        print("[❌] Validation failed:", e)

def insert_data(repo_link: str, result: str):
    REPO_LINK = repo_link.split("github.com/")[-1].replace(".git", "").strip()
    data = {
        "repo_link": REPO_LINK,
        "result": result,
    }
    try:
        upsert_migration(data)
        return True
    except Exception as e:
        print("[❌] Upsert failed:", e)
        return False