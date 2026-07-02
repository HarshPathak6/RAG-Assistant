from langchain_community.document_loaders import UnstructuredMarkdownLoader


def load_markdown(file_path: str):
    """
    Loads a Markdown file and returns LangChain Document objects.
    """

    loader = UnstructuredMarkdownLoader(file_path)

    documents = loader.load()

    return documents