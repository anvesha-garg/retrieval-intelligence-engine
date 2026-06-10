from langchain_groq import ChatGroq


def summarize_documents(vectordb):

    docs = vectordb.similarity_search(
        "summarize document",
        k=20
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
Generate a professional executive summary
of the uploaded document.

Include:

1. Main Topic
2. Key Findings
3. Important Information
4. Overall Purpose

Document:

{context}
"""

    response = llm.invoke(prompt)

    return response.content