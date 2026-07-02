from importlib.resources import path
from pathlib import Path
import shutil
from Splitters.TextSplitter import split_documents
from fastapi import APIRouter, UploadFile, File, HTTPException
from Loaders.PDFLoader import load_pdf
from Loaders.DOCXLoader import load_docx
from Loaders.TXTLoader import load_txt
from Loaders.MarkdownLoader import load_markdown
from VectorStore.ChromaDB import create_vector_store


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "uploads"

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = Path(UPLOAD_FOLDER) / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        documents = load_pdf(file_path)

    elif extension == ".docx":
        documents = load_docx(file_path)

    elif extension == ".txt":
        documents = load_txt(file_path)

    elif extension == ".md":
        documents = load_markdown(file_path)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    chunks = split_documents(documents)

    vector_store = create_vector_store(chunks)

    return {
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks),
        "message": "Embeddings created and stored successfully."
    }