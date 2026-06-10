from langchain_groq import ChatGroq


def ask_question(question, vectordb):

    docs = vectordb.similarity_search(
        question,
        k=6
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
You are Retrieval Intelligence Engine (RIE).

Answer ONLY from the provided context.

If the answer cannot be found in the context,
respond with:

"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content, docs