from fastapi import APIRouter
from Schemas.RequestSchemas import ChatRequest
from Chains.RetrievalChain import ask_question
from Schemas.ResponseSchemas import ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = ask_question(request.question)
    return result