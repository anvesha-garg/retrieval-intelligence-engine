from utils.summarizer import summarize_documents
import tempfile
import streamlit as st

from utils.pdf_processor import process_pdf
from utils.vectordb import create_vector_store
from utils.rag import ask_question

# --------------------
# PAGE CONFIG
# --------------------

st.set_page_config(
    page_title="Retrieval Intelligence Engine (RIE)",
    page_icon="📚",
    layout="wide"
)

# --------------------
# SESSION STATE
# --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

# --------------------
# SIDEBAR
# --------------------

with st.sidebar:

    st.header("⚙️ RIE Control Panel")

    theme = st.selectbox(
        "Choose Theme",
        [
            "Cyber Blue",
            "Dark AI",
            "Minimal Light"
        ]
    )

    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🚀 Build Knowledge Base"):

        if not uploaded_files:

            st.warning("Please upload at least one PDF.")

        else:

            st.session_state.vectordb = None

            all_chunks = []

            progress = st.progress(0)

            total = len(uploaded_files)

            for index, file in enumerate(uploaded_files):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(file.read())

                    chunks = process_pdf(tmp.name)

                    all_chunks.extend(chunks)

                progress.progress(
                    (index + 1) / total
                )

            st.session_state.vectordb = create_vector_store(
                all_chunks
            )

            st.success(
                f"Knowledge Base Created ({len(all_chunks)} chunks)"
            )

    st.divider()

    if st.button("📝 Generate Summary"):

        if st.session_state.vectordb is None:

            st.error(
                "Please build the knowledge base first."
            )

        else:

            summary = summarize_documents(
                st.session_state.vectordb
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": summary
                }
            )

            st.success("Summary Generated")

    st.divider()

    if st.button("🗑️ Delete Knowledge Base"):

        st.session_state.vectordb = None
        st.session_state.messages = []

        st.success(
            "Knowledge Base Deleted"
        )

    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.success(
            "Chat Cleared"
        )

# --------------------
# THEMES
# --------------------

if theme == "Cyber Blue":

    st.markdown(
        """
        <style>

        .stApp {
            background-color:#0A192F;
        }

        h1 {
            color:#64FFDA;
        }

        .stChatMessage {
            border-radius:15px;
            padding:10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

elif theme == "Dark AI":

    st.markdown(
        """
        <style>

        .stApp {
            background-color:#111827;
        }

        h1 {
            color:#60A5FA;
        }

        .stChatMessage {
            border-radius:15px;
            padding:10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <style>

        .stApp {
            background-color:#F8FAFC;
        }

        h1 {
            color:#2563EB;
        }

        .stChatMessage {
            border-radius:15px;
            padding:10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# --------------------
# HEADER
# --------------------

st.title("📚 Retrieval Intelligence Engine (RIE)")

st.markdown(
    """
### AI-Powered Document Intelligence Platform

Upload PDFs, build a knowledge base,
generate summaries, and ask questions
using Retrieval-Augmented Generation (RAG).
"""
)

# --------------------
# CHAT HISTORY
# --------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# --------------------
# CHAT INPUT
# --------------------

query = st.chat_input(
    "Ask a question about your documents..."
)

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    if st.session_state.vectordb is None:

        final_response = """
No knowledge base detected.

Please upload PDFs and build a knowledge base first.
"""

    else:

        answer, docs = ask_question(
            query,
            st.session_state.vectordb
        )

        source_text = "\n\n### Sources\n"

        pages = []

        for doc in docs:

            page = doc.metadata.get(
                "page",
                "Unknown"
            )

            try:

                pages.append(
                    f"Page {page + 1}"
                )

            except:

                pages.append(
                    str(page)
                )

        unique_pages = list(
            set(pages)
        )

        source_text += "\n".join(
            [
                f"- {page}"
                for page in unique_pages
            ]
        )

        final_response = (
            answer +
            source_text
        )

    with st.chat_message("assistant"):

        st.markdown(
            final_response
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_response
        }
    )

# --------------------
# DOWNLOAD CHAT
# --------------------

if st.session_state.messages:

    chat_history = ""

    for msg in st.session_state.messages:

        chat_history += (
            f"{msg['role'].upper()}:\n"
            f"{msg['content']}\n\n"
        )

    st.download_button(
        label="📥 Download Chat History",
        data=chat_history,
        file_name="rie_chat_history.txt",
        mime="text/plain"
    )