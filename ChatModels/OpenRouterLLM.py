from langchain_openai import ChatOpenAI

from config import settings


llm = ChatOpenAI(
    model=settings.OPENROUTER_QWEN_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

llm2 = ChatOpenAI(
    model=settings.OPENROUTER_DEEPSEEK_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)