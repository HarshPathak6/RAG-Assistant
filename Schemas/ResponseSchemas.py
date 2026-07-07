from pydantic import BaseModel
from typing import List


class Citation(BaseModel):
    document: str
    page: int

class ChatResponse(BaseModel):
    question: str
    answer: str
    citations: List[Citation]