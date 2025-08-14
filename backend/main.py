from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class UploadResponse(BaseModel):
    doc_id:str
    status:str

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{doc_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: Save {doc_id, status: "uploaded"} to Postgres

    return {"doc_id": doc_id, "status": "uploaded"}
