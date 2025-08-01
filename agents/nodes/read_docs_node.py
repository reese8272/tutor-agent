"""Node responsible for retrieving documentation from a vector store."""

from typing import List
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from agents.state import TutorAgentState


# Load environment variables so embedding credentials are available
load_dotenv(override=True)


async def retrieve_context_from_docs(state: TutorAgentState) -> TutorAgentState:
    """Retrieve relevant documentation chunks using a similarity search.

    Expects the user's input (concept name or query) to be stored on
    ``state.user_input``. Uses a local FAISS vector store to find the top k
    documents related to the query and stores their page contents on
    ``state.retrieved_chunks`` for downstream question generation.

    Parameters
    ----------
    state : TutorAgentState
        The current agent state.

    Returns
    -------
    TutorAgentState
        The updated state with ``retrieved_chunks`` populated.
    """
    if not state.user_input:
        raise ValueError("No user input provided to retrieve context.")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        "embeddings/vector_store",
        embeddings,
        allow_dangerous_deserialization=True,
    )

    docs = vectorstore.similarity_search(state.user_input, k=4)
    retrieved_text: List[str] = [doc.page_content for doc in docs]
    state.retrieved_chunks = retrieved_text
    return state


# Alias used when adding this node to a graph
node = retrieve_context_from_docs