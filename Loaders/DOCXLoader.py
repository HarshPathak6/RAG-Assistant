from langchain_community.document_loaders import Docx2txtLoader


def load_docx(file_path: str):
    """
    Loads a DOCX and returns LangChain Document objects.
    """

    loader = Docx2txtLoader(file_path)

    documents = loader.load()

    return documents