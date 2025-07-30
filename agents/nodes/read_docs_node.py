### FILE: read_docs_node.py
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from agents.state import TutorAgentState

def retrieve_context_from_docs(state: TutorAgentState) -> TutorAgentState:
    print("[🔍] Retrieving relevant context from FAISS vectorstore...")

    if not state.user_input:
        raise ValueError("No user input provided to retrieve context.")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        "embeddings/vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(state.user_input, k=4)
    retrieved_text = [doc.page_content for doc in docs]

    return state.model_copy(update={"retrieved_chunks": retrieved_text})

