import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from pathlib import Path

VECTORSTORE_PATH = Path("embeddings/user_answers")

def embed_texts_and_save(texts, metadatas, namespace="user_answers"):
    """Embed a list of text chunks and save to a namespaced FAISS index."""
    try:
        if not texts:
            print("[ℹ️] No texts to embed.")
            return

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        docs = [
            Document(page_content=txt, metadata=meta)
            for txt, meta in zip(texts, metadatas)
        ]

        vectorstore = FAISS.from_documents(docs, embedding=embeddings)
        VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(VECTORSTORE_PATH))

        print(f"[✅] Embedded and saved {len(texts)} correct answers to {VECTORSTORE_PATH}")

    except Exception as e:
        print(f"[❌] Embedding failed: {e}")
