from langchain_chroma import Chroma

from Embeddings.EmbeddingModel import embeddings
from ChatModels.OpenRouterLLM import llm, llm2
from Prompts.RagPrompt import rag_prompt


vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


def ask_question(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = rag_prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    response = llm2.invoke(prompt)

    return response.content