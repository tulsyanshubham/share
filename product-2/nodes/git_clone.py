import os
import shutil
import subprocess
from urllib.parse import urlparse

def handle_remove_readonly(func, path, exc_info):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)
    
async def clone_repo(repo_url: str, destination_dir: str = "./cloned_repo"):
    try:
        if os.path.exists(destination_dir):
            print(f"[INFO] Destination '{destination_dir}' already exists. Removing it first...")
            # subprocess.run(["rm", "-rf", destination_dir], check=True)
            shutil.rmtree(destination_dir, onerror=handle_remove_readonly)

        print(f"[INFO] Cloning repo from {repo_url} to {destination_dir}...")
        subprocess.run(["git", "clone", repo_url, destination_dir], check=True)
        print("[SUCCESS] Repo cloned successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to clone repository: {e}")
        return False

# if __name__ == "__main__":
#     repo_url = "https://github.com/sivaprasadreddy/spring-modular-monolith.git"  # replace this
#     destination = "./monolith_code"  # change if you want a different dir
#     clone_repo(repo_url, destination)