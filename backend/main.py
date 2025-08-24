from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import get_db_connection
import db_queries
from pydantic import BaseModel
import uuid
import shutil
import os

app = FastAPI()

# Establish CORS credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database
db_queries.create_table()

class UploadResponse(BaseModel):
    doc_id:str
    status:str

# Endpoint to upload documents
@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{doc_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save {doc_id, status: "uploaded"} to Postgres
    db_queries.insert_research(doc_id, file.filename, "uploaded", file_path)

    return {"doc_id": doc_id, "status": "uploaded"}

# Endpoint to fetch documents and their related data
@app.get("/documents")
async def get_documents():
    documents = db_queries.get_all_research()
    return {"documents": documents}

# Endpoint to delete specific documents and their related data
@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    db_queries.delete_research(doc_id)
    return {"status": "deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)