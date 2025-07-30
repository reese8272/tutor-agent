# agents/nodes/read_docs_node.py

from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_openai import OpenAIEmbeddings  # ✅ FIXED
from langchain_community.vectorstores import FAISS
from agents.state import TutorAgentState


def retrieve_context_from_docs(state: TutorAgentState) -> TutorAgentState:
    """Retrieve relevant documentation chunks based on user input."""
    print("[🔍] Retrieving relevant context from FAISS vectorstore...")

    if not state.user_input:
        raise ValueError("No user input provided to retrieve context.")

    embeddings = OpenAIEmbeddings()

    # ✅ Make sure `vectorstore_path` is a **folder**, not a file path
    vectorstore = FAISS.load_local(
        state.vectorstore_path,  # ← should be something like: "embeddings/vector_store"
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(state.user_input, k=4)
    retrieved_text = [doc.page_content for doc in docs]

    return state.model_copy(update={"retrieved_chunks": retrieved_text})
