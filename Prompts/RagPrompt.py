from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template("""
You are an intelligent AI assistant.

You are provided with document context.

Answer using ONLY the provided context whenever the answer exists.

If the answer is only partially present,
complete it with your own knowledge and clearly indicate what comes from the document.

If the answer is completely unrelated to the uploaded documents,
answer using your own general knowledge.

Never invent document information.

Context:
{context}

Question:
{question}

Answer:
""")