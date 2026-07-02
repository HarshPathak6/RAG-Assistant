from fastapi import APIRouter
from Schemas.RequestSchemas import ChatRequest
from Schemas.ResponseSchemas import ChatResponse
from Chains.RetrievalChain import ask_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    answer = ask_question(request.question)

    return ChatResponse(
        question=request.question,
        answer=answer
    )