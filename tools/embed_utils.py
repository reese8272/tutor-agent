from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from pathlib import Path
import pickle

def embed_chunks(chunks: list, persis_path: str = "embeddings/vector_store"):
    """Embeds and persists chunks using FAISS."""
    print(f"[+] Embedding chunks with OpenAIEmbeddings...")
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)

    Path(persis_path).parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(persis_path)
    print(f"[✓] Vector store saved to: {persis_path}")

def load_vectorstore(persis_path: str = "embeddings/vector_store.faiss"):
    """Loads a persisted FAISS vector store."""
    print(f"[+] Leading vector store...")
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(persis_path, embeddings)