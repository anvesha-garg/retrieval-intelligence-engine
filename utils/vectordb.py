from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vectordb = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectordb