from fastapi import FastAPI
from Routers.UploadRouter import router as upload_router
from Routers.ChatRouter import router as chat_router

app = FastAPI(
    title="RAG API",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {
        "message": "RAG API is running."
    }