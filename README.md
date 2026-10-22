# Multi-Format RAG Document Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents, ask questions about their contents, and receive AI-generated answers grounded in retrieved document context, along with source citations.

Built with **Python, FastAPI, LangChain, ChromaDB, Hugging Face Embeddings, and OpenRouter**, the application supports multiple document formats and uses semantic similarity search to retrieve relevant information before generating an answer.

## Features

- **Multi-format document ingestion:** Upload PDF, DOCX, TXT, and Markdown files.
- **Document loading:** Extracts text and metadata using format-specific LangChain document loaders.
- **Text chunking:** Splits documents into smaller, overlapping chunks to improve retrieval.
- **Semantic search:** Uses Hugging Face embeddings and ChromaDB to retrieve relevant document chunks.
- **Retrieval-Augmented Generation:** Supplies retrieved context to an LLM before generating an answer.
- **Source citations:** Returns document names and page metadata associated with retrieved chunks.
- **Multiple LLM configurations:** Configures OpenRouter models for different language-model tasks.
- **REST API:** Exposes upload and chat functionality through FastAPI.
- **Persistent vector storage:** Stores document embeddings in a local ChromaDB directory.
- **Interactive API documentation:** Supports testing endpoints through Swagger UI.

## Architecture

```text
                  User
                   |
                   v
                FastAPI
                   |
          +--------+--------+
          |                 |
          v                 v
     Upload Router      Chat Router
          |                 |
          v                 v
    Document Loaders   Retrieval Chain
          |                 |
          v                 v
      Text Splitter    Semantic Search
          |                 |
          v                 v
    Hugging Face       ChromaDB
      Embeddings       Vector Store
          |                 |
          v                 v
    Store Chunks      Retrieved Context
                            |
                            v
                       RAG Prompt
                            |
                            v
                    OpenRouter LLM
                            |
                            v
                  Answer + Citations
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | REST API and request handling |
| Uvicorn | ASGI application server |
| LangChain | Document processing, embeddings integration, prompts, and retrieval |
| OpenRouter | Access to configured LLMs |
| Hugging Face Embeddings | Converts document chunks into vector embeddings |
| ChromaDB | Stores and retrieves document embeddings |
| Pydantic Settings | Loads configuration from environment variables |
| python-multipart | Handles file uploads through FastAPI |

## Project Structure

```text
RAG-Assistant/
│
├── ChatModels/
│   └── OpenRouterLLM.py
│
├── Chains/
│   └── RetrievalChain.py
│
├── Embeddings/
│   └── EmbeddingModel.py
│
├── Loaders/
│   ├── PDFLoader.py
│   ├── DOCXLoader.py
│   ├── TXTLoader.py
│   └── MarkdownLoader.py
│
├── Prompts/
│   └── RagPrompt.py
│
├── Routers/
│   ├── ChatRouter.py
│   └── UploadRouter.py
│
├── Schemas/
│   ├── RequestSchemas.py
│   └── ResponseSchemas.py
│
├── Splitters/
│   └── TextSplitter.py
│
├── VectorStore/
│   └── ChromaDB.py
│
├── config.py
├── main.py
├── requirements.txt
├── test.py
└── .gitignore
```

Runtime-generated directories:

```text
uploads/       Uploaded source documents
chroma_db/     Persistent ChromaDB vector store
```

These directories are excluded from Git by the project's `.gitignore`.

## How It Works

### 1. Document Upload

The application accepts documents through the upload endpoint. The file extension determines which loader processes the document.

Supported formats:

| Format | Loader |
|---|---|
| PDF | `PyPDFLoader` |
| DOCX | `Docx2txtLoader` |
| TXT | `TextLoader` |
| Markdown | `UnstructuredMarkdownLoader` |

### 2. Text Splitting

Loaded documents are divided into smaller chunks using `RecursiveCharacterTextSplitter`.

Current configuration:

- **Chunk size:** 1,000 characters
- **Chunk overlap:** 200 characters

Overlapping chunks help preserve context between adjacent sections of a document.

### 3. Embedding Generation and Storage

The configured Hugging Face embedding model converts the document chunks into vector representations.

ChromaDB stores these vectors alongside their associated document content and metadata in the `chroma_db/` directory.

### 4. Semantic Retrieval

When a user submits a question, the retrieval chain performs a similarity search against the ChromaDB vector store.

The current implementation retrieves the top four matching chunks.

### 5. Answer Generation

The retrieved content and user question are inserted into a LangChain prompt template. The configured DeepSeek model on OpenRouter generates the response using the retrieved context and the prompt's instructions.

### 6. Citations

The API returns citation metadata for the retrieved chunks, including the source document and page metadata when available.

Citations identify retrieved sources; they do not guarantee that every statement in the answer is directly supported by those sources.

## Installation and Setup

### Prerequisites

- Python installed.
- An OpenRouter API key.
- Internet access for the configured OpenRouter model and initial embedding-model downloads.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Assistant.git
cd RAG-Assistant
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the URL if your repository has a different name.

### 2. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a document loader reports a missing optional dependency, install the package required by that loader. For example, the DOCX and Markdown loaders may require additional loader-specific dependencies depending on your environment.

### 4. Configure Environment Variables

Create a `.env` file in the project root, alongside `main.py` and `config.py`.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_QWEN_MODEL=your_qwen_model_id
OPENROUTER_DEEPSEEK_MODEL=your_deepseek_model_id
EMBEDDING_MODEL=your_huggingface_embedding_model
```

Replace the example values with your actual configuration.

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | API key for OpenRouter |
| `OPENROUTER_QWEN_MODEL` | OpenRouter model configured for `llm` |
| `OPENROUTER_DEEPSEEK_MODEL` | OpenRouter model configured for `llm2`, used by the retrieval chain |
| `EMBEDDING_MODEL` | Hugging Face embedding model identifier |

The application loads these values through Pydantic Settings in `config.py`.

**Security:** Never commit your `.env` file or expose API keys in your source code.

## Running the Application

Start the FastAPI server from the project root:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Open the interactive Swagger UI to test the endpoints:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. Health Check

**Method:** `GET`

**Endpoint:** `/`

Checks whether the API is running.

Example response:

```json
{
  "message": "RAG API is running."
}
```

### 2. Upload a Document

**Method:** `POST`

**Endpoint:** `/upload/`

Uploads and processes a supported document, splits it into chunks, generates embeddings, and stores them in ChromaDB.

Use `multipart/form-data` with a file field named `file`.

Supported extensions:

- `.pdf`
- `.docx`
- `.txt`
- `.md`

Example response:

```json
{
  "filename": "sample.pdf",
  "pages": 10,
  "chunks": 15,
  "message": "Embeddings created and stored successfully."
}
```

The numbers above are illustrative; actual counts depend on the uploaded document.

### 3. Ask a Question

**Method:** `POST`

**Endpoint:** `/chat/`

Request body:

```json
{
  "question": "What are the main points discussed in the uploaded document?"
}
```

Example response:

```json
{
  "question": "What are the main points discussed in the uploaded document?",
  "answer": "The document discusses its main objectives, key concepts, and conclusions...",
  "citations": [
    {
      "document": "uploads/sample.pdf",
      "page": 2
    }
  ]
}
```

The answer and citation values are illustrative. Actual responses depend on the indexed documents, retrieved chunks, and LLM output.

## Example Workflow

1. Start the FastAPI server.
2. Open `/docs` in your browser.
3. Use `POST /upload/` to upload a document.
4. Wait for document loading, chunking, embedding generation, and vector storage to finish.
5. Use `POST /chat/` to submit a question about the uploaded content.
6. Inspect the generated answer and returned source citations.

## Configuration and Implementation Details

### LLM Integration

The application uses LangChain's `ChatOpenAI` wrapper to communicate with OpenRouter through its API-compatible endpoint:

```text
https://openrouter.ai/api/v1
```

Two model instances are configured in `ChatModels/OpenRouterLLM.py`. The retrieval chain currently uses `llm2` to generate the final answer.

### Embeddings

The embedding model is configured in `Embeddings/EmbeddingModel.py` and selected through the `EMBEDDING_MODEL` environment variable.

Use the same embedding model configuration when indexing and querying the vector store so that the vectors remain compatible.

### Vector Store

The ChromaDB vector store is persisted in:

```text
chroma_db/
```

The retrieval chain loads the persisted store and performs similarity search over its indexed chunks.

### Prompt Template

`Prompts/RagPrompt.py` defines the instructions and context format supplied to the LLM. The prompt prioritizes document context when relevant, while allowing general-knowledge answers when the uploaded documents do not address the question.

## Current Limitations

- The application exposes a REST API; a dedicated chat frontend is not included in the current repository.
- The chat endpoint does not accept a document or project identifier. It queries the configured shared ChromaDB collection.
- Citations are derived from retrieved chunk metadata and may not correspond to independently verified claims.
- Retrieval quality depends on document extraction, chunking, the embedding model, and the similarity search results.
- The application does not currently provide user authentication or per-user document isolation.
- Uploaded documents are processed locally, and the vector store is persisted locally unless the deployment environment provides another storage arrangement.
- Generated answers may be incomplete or inaccurate and should be checked against the original sources when accuracy is important.

## Future Improvements

- Build a chat interface using Streamlit or React.
- Add conversation history and multi-turn chat support.
- Add document management and deletion endpoints.
- Support document collections and per-user retrieval.
- Improve citation accuracy by including relevant excerpts and page references.
- Add configurable retrieval parameters and relevance filtering.
- Add streaming responses for a more interactive experience.
- Add automated tests for document loaders, retrieval, and API endpoints.
- Add tracing and observability for LLM calls and retrieval operations.

## License

No license has been specified in the project files. Add a `LICENSE` file if you intend to publish the repository under a particular open-source license.

## Acknowledgements

Built using FastAPI, LangChain, ChromaDB, Hugging Face, and OpenRouter.
