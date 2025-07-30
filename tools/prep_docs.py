# tools/prep_docs.py

import pickle
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from tools.doc_loader import load_docs_from_directory, split_documents
from dotenv import load_dotenv

load_dotenv(override=True)


DOCS_DIR = "docs"
RAW_CHUNKS_PATH = "data/raw_docs.pkl"
VECTORSTORE_PATH = "embeddings/vector_store"

def prepare_and_index_docs():
    print("[📚] Loading and splitting docs...")
    docs = load_docs_from_directory(DOCS_DIR)
    chunks = split_documents(docs)

    print(f"[💾] Saving {len(chunks)} chunks to {RAW_CHUNKS_PATH}")
    Path(RAW_CHUNKS_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("[🧠] Embedding and indexing chunks...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    Path(VECTORSTORE_PATH).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)

    print(f"[✅] Vectorstore saved to {VECTORSTORE_PATH}")


if __name__ == "__main__":
    prepare_and_index_docs()
