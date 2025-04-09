from nodes.repo_scan import repo_scan
from nodes.file_split import file_split
from fastapi import FastAPI,Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from nodes.test import check_api_keys
from nodes.folder_structure import folder_structure
from nodes.insert_data import insert_data
from nodes.check_db import check_db
# from config.logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
async def scan(git_url: str = Form(...)):
    repo_data = repo_scan(git_url)
    return JSONResponse(content=repo_data)
    
@app.post("/split")
async def root(git_url: str = Form(...)):
    repo_data = repo_scan(git_url)
    microservices, file_descriptions, nested_output = file_split(repo_data)
    return JSONResponse(content=nested_output)
    
@app.post("/structure")
async def root(git_url: str = Form(...)):
    repo_data = repo_scan(git_url)
    microservices, file_descriptions, nested_output = file_split(repo_data)
    structure = folder_structure(microservices, file_descriptions)
    return JSONResponse(content={"file_split":nested_output,"folder_structure":structure})

@app.post("/check")
async def check(git_url: str = Form(...)):
    found,data = check_db(git_url)
    if not found:
        return JSONResponse(content={"Success":found,"data":None})
    return JSONResponse(content={"Success":found,"data":data})

@app.post("/insert")
async def insert(git_url: str = Form(...)):
    repo_data = repo_scan(git_url)
    microservices, file_descriptions, nested_output = file_split(repo_data)
    structure = folder_structure(microservices, file_descriptions)
    success = insert_data(git_url, nested_output, structure)
    return JSONResponse(content={"success":success,"file_split":nested_output,"folder_structure":structure})
    
@app.get("/test")
async def test():
    return JSONResponse(content=check_api_keys())

