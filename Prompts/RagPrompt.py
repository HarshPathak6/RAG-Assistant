from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Use the retrieved context as your primary source.

If the answer exists in the context, answer using it.

If the context is incomplete, use your own general knowledge to provide a correct answer, but clearly distinguish which parts come from your own knowledge.

Retrieved Context:
{context}

Question:
{question}
"""
)