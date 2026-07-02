from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Use ONLY the context below to answer.

If the answer is not found in the context,
reply with:

"I couldn't find that information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""
)