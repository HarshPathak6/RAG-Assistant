from langchain_chroma import Chroma
from Embeddings.EmbeddingModel import embeddings
from ChatModels.OpenRouterLLM import llm, llm2
from Prompts.RagPrompt import rag_prompt

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


def ask_question(question: str):

    # Semantic search
    docs = vector_store.similarity_search_with_score(
        question,
        k=4
    )

    context = ""

    citations = []

    for doc, score in docs:

        context += doc.page_content + "\n\n"

        citations.append(
            {
                "document": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0)
            }
        )

    prompt = rag_prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    response = llm2.invoke(prompt)

    return {
        "question": question,
        "answer": response.content,
        "citations": citations
    }