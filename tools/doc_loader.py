from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import pickle

def load_docs_from_directory(directory: str, file_extension: str = ".md") -> list:
    """Loads all documentation files from a given directory."""
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory {directory} not found.")
    
    loader = DirectoryLoader(
        path,
        glob=f"**/*{file_extension}",
        loader_cls=TextLoader,
        show_progress=True,
    )

    print(f"[+] Loading Documents from: {directory}")
    return loader.load()


def split_documents(docs: list, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Splits raw documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    print(f"[+] Splitting {len(docs)} documents into chunks...")
    return splitter.split_documents(docs)


def save_chunks(chunks: list, output_path: str = "data/raw_docs.pkl") -> None:
    """Saves the split documents to disk for inspection/debugging."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(chunks, f)
    print(f"[✓] Saved {len(chunks)} chunks to {output_path}")
