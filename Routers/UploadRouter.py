from pathlib import Path
import shutil
from Splitters.TextSplitter import split_documents
from fastapi import APIRouter, UploadFile, File, HTTPException
from Loaders.PDFLoader import load_pdf
from VectorStore.ChromaDB import create_vector_store

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "uploads"

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    file_path = Path(UPLOAD_FOLDER) / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    documents = load_pdf(str(file_path))

    chunks = split_documents(documents)

    vector_store = create_vector_store(chunks)

    return {
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks),
        "message": "Embeddings created and stored successfully."
    }
