from langchain_chroma import Chroma

from Embeddings.EmbeddingModel import embeddings


def create_vector_store(chunks):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return vector_store