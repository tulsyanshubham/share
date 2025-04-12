from pydantic import BaseModel
from typing import Dict

class MigrationSchema(BaseModel):
    repo_link: str
    result: str
