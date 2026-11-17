from langchain_ollama import ChatOllama
from retriever import get_retriever
retriever = get_retriever()
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    num_predict=500,
    reasoning=False
)
def answer_question(query):
    retrieved_docs = retriever.invoke(query)
    if not retrieved_docs:
        return (
            "I couldn't find this information in the "
            "available IT knowledge base. Please contact "
            "your IT support team.",
            []
        )
    context_parts = []
    for index, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get("source", "Unknown source")
        context_parts.append(
            f"""
            DOCUMENT {index}
            SOURCE: {source}
            CONTENT:
            {doc.page_content}
            """
        )
    context = "\n\n".join(context_parts)
    prompt = f"""
You are an IT support assistant.
Answer the user's question using ONLY the supplied documents.
STRICT RULES:
1. Do not use your general knowledge.
2. Do not add any troubleshooting step that is not
   explicitly written in the documents.
3. Do not invent commands, shortcuts, percentages,
   URLs, software names, or procedures.
4. Do not expand a documented step with additional
   instructions or assumptions.
5. If a detail is not documented, do not include it.
6. Use only the relevant information.
7. If the documents do not contain enough information,
   say that the knowledge base does not contain the answer.
8. Keep the answer concise and easy to follow.
9. Mention the source filename.
DOCUMENTS:
{context}
USER QUESTION:
{query}
Write the answer:
"""
    response = llm.invoke(prompt)
    sources = sorted({
        doc.metadata.get("source", "Unknown source")
        for doc in retrieved_docs
    })
    return response.content, sources