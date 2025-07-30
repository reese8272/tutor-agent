import os
import shutil
from pathlib import Path
import subprocess

# ------------------------
# Constants
# ------------------------

UNCLEANED_DIR = Path("uncleaned_docs")
CLEANED_LANGCHAIN_DIR = Path("docs/langchain")
CLEANED_LANGGRAPH_DIR = Path("docs/langgraph")

LANGCHAIN_REPO = "https://github.com/langchain-ai/langchain.git"
LANGGRAPH_REPO = "https://github.com/langchain-ai/langgraph.git"

LANGCHAIN_REPO_DIR = UNCLEANED_DIR / "langchain_repo"
LANGGRAPH_REPO_DIR = UNCLEANED_DIR / "langgraph_repo"

ALLOWED_EXTENSIONS = [".md", ".txt", ".html"]


# ------------------------
# Helpers
# ------------------------

def run_command(command: str):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[❌] Failed to run: {command}\n{e}")

def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[⚠️] Failed to read {path}: {e}")
        return ""

def safe_write_text(dest: Path, content: str):
    try:
        dest.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"[⚠️] Failed to write {dest}: {e}")

def flatten_path(path: Path) -> str:
    """Creates a flat filename from a full path."""
    parts = path.relative_to(path.parents[2]).with_suffix('').parts
    return "_".join(parts) + path.suffix

def copy_relevant_files(src_dir: Path, dest_dir: Path, label: str):
    print(f"[↪] Copying files from {label} repo...")
    count = 0
    for file_path in src_dir.rglob("*"):
        if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
            flat_name = flatten_path(file_path)
            dest_path = dest_dir / flat_name
            content = safe_read_text(file_path)
            if content:
                safe_write_text(dest_path, content)
                count += 1
    print(f"[✅] {count} files copied to {dest_dir}")


# ------------------------
# Main Pipeline
# ------------------------

def clone_and_extract_docs():
    UNCLEANED_DIR.mkdir(exist_ok=True)
    CLEANED_LANGCHAIN_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_LANGGRAPH_DIR.mkdir(parents=True, exist_ok=True)

    if LANGCHAIN_REPO_DIR.exists():
        print("[ℹ️] LangChain repo already cloned. Skipping.")
    else:
        print("[🔄] Cloning LangChain...")
        run_command(f"git clone --depth=1 {LANGCHAIN_REPO} {LANGCHAIN_REPO_DIR}")

    if LANGGRAPH_REPO_DIR.exists():
        print("[ℹ️] LangGraph repo already cloned. Skipping.")
    else:
        print("[🔄] Cloning LangGraph...")
        run_command(f"git clone --depth=1 {LANGGRAPH_REPO} {LANGGRAPH_REPO_DIR}")

    copy_relevant_files(LANGCHAIN_REPO_DIR, CLEANED_LANGCHAIN_DIR, "LangChain")
    copy_relevant_files(LANGGRAPH_REPO_DIR, CLEANED_LANGGRAPH_DIR, "LangGraph")


# ------------------------
# Entrypoint
# ------------------------

if __name__ == "__main__":
    clone_and_extract_docs()
