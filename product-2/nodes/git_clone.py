import os
import subprocess
from urllib.parse import urlparse

def clone_repo(repo_url: str, destination_dir: str = "./cloned_repo"):
    try:
        if os.path.exists(destination_dir):
            print(f"[INFO] Destination '{destination_dir}' already exists. Removing it first...")
            subprocess.run(["rm", "-rf", destination_dir], check=True)

        print(f"[INFO] Cloning repo from {repo_url} to {destination_dir}...")
        subprocess.run(["git", "clone", repo_url, destination_dir], check=True)
        print("[SUCCESS] Repo cloned successfully.")
        return destination_dir
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to clone repository: {e}")
        return None

# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/sivaprasadreddy/spring-modular-monolith.git"  # replace this
    destination = "./monolith_code"  # change if you want a different dir
    clone_repo(repo_url, destination)