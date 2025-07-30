# 🧠 LangGraph Tutor Agent

An **AI-powered interactive tutor** that reads LangChain and LangGraph documentation, quizzes you with open-ended concept and coding questions, and evolves based on what you've already mastered. Powered by LangGraph, LangChain, and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **Documentation Ingestion**  
  Parses and chunks local LangChain and LangGraph documentation for intelligent retrieval.

- **Interactive Agent Tutor**  
  Learns from docs, quizzes you like a human tutor (concepts + coding), and chats naturally.

- **Smart Question Tracking**  
  Logs what you’ve been taught and intelligently suggests new material you haven’t mastered.

- **RAG Database Logging**  
  All Q&A interactions are stored and indexed for long-term personalized learning.

## 🗂️ Project Structure

```
langgraph_tutor_agent/
├── docs/                   # Local documentation (LangChain, LangGraph)
├── embeddings/             # FAISS/Chroma vector store
├── logs/                   # All question/answer logs (JSON)
├── data/                   # Chunked docs and metadata
├── agents/                 # LangGraph nodes and graph logic
├── tools/                  # Utility functions (loading, embedding, etc.)
├── prompts/                # Prompt engineering for nodes
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 📦 Installation

```bash
git clone https://github.com/your-username/langgraph-tutor-agent.git
cd langgraph_tutor_agent
pip install -r requirements.txt
```

## 🧪 Usage

```bash
python main.py
```

Follow the interactive prompt. The agent will teach, quiz, and learn with you.

## 🔧 Configuration

- Add your LangChain/LangGraph docs to `./docs/`
- Customize chunking or embedding settings in `tools/doc_loader.py`
- Prompts are editable in `./prompts/`

## 📚 Example Interaction

> **Agent:** “What is the role of a `StateGraph` in LangGraph?”  
> **You:** “It defines the agent’s node flow and state transitions.”  
> **Agent:** “Correct. Can you now implement a minimal `StateGraph` with two nodes?”

## 🧠 Tech Stack

- Python 3.11+
- LangChain + LangGraph
- FAISS / Chroma
- OpenAI (or any LLM with tool-calling)
- Pydantic

## 📈 Roadmap

- [x] Local doc ingestion + RAG
- [x] Interactive Q&A chatbot
- [ ] Visual progress dashboard
- [ ] LangGraph code auto-annotator (future)

## 🧑‍💻 Maintained By

**Reese Ludwick**  
_Computer Science @ Shepherd University_  
_Machine Learning • LangGraph • Agentic Workflows_

## 📄 License

MIT License
