from pydantic import BaseModel
from typing import Dict

class MigrationSchema(BaseModel):
    repo_link: str
    file_split: Dict
    folder_structure: str
