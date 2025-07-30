# 🧠 LangGraph Tutor Agent

An **AI-powered interactive tutor** that reads LangChain and LangGraph documentation, quizzes you with open-ended concept and coding questions, and evolves based on what you've already mastered. Powered by LangGraph, LangChain, and Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- **Documentation Ingestion**  
  Parses and chunks local LangChain and LangGraph documentation for intelligent retrieval.

- **Interactive Agent Tutor**  
  Learns from docs, quizzes you like a human tutor (concepts + coding), and chats naturally.

- **Smart Question Tracking**  
  Logs what you’ve been taught and intelligently suggests new material you haven’t mastered.

- **Review Mode**  
  Revisits previously asked questions and generates follow-up quizzes from your past answers.

- **Gradio + CLI Support**  
  Use it in the browser or directly from the terminal.

---

## 🗂️ Project Structure

```
langgraph_tutor_agent/
├── docs/                   # Raw .md documentation (LangChain, LangGraph, etc.)
├── data/
│   └── concepts.json       # Concept IDs, keywords, and prerequisites
├── embeddings/
│   └── vector_store/       # FAISS vector index
├── logs/
│   └── question_log.json   # All session Q&A logs
├── agents/
│   ├── state.py            # Pydantic state for LangGraph
│   ├── tutor_agent.py      # Graph logic for learn/review
│   └── nodes/
│       ├── generate_questions.py
│       ├── chat_node.py
│       ├── generate_feedback_node.py
│       ├── suggest_next_node.py
│       ├── store_answers_node.py
│       ├── review_node.py
│       └── read_docs_node.py
├── prompts/                # Prompt templates for each agent node
├── tools/
│   ├── doc_loader.py
│   └── prep_docs.py
├── web/
│   └── ui.py               # Gradio web UI
├── main.py                 # CLI interface
├── requirements.txt
└── README.md
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/langgraph-tutor-agent.git
cd langgraph_tutor_agent
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Then create a `.env` file:
```
OPENAI_API_KEY=your-key-here
```

---

## 🧠 Setup: Preparing Documentation

1. Drop Markdown `.md` files into the `docs/` folder.
2. Run the prep script:
```bash
python tools/prep_docs.py
```

---

## 🧪 Usage

### Run via CLI

```bash
python main.py
```

- Choose between `learn` and `review` mode
- Get questions and answer them in the terminal
- Receive AI feedback and new concept suggestions

### Run via Gradio UI

```bash
python web/ui.py
```

- Interact with the tutor in your browser
- Type answers into form fields
- Receive feedback and suggestion in real-time

---

## 📚 Concept Mapping

To track your learning progress, define your curriculum in `data/concepts.json`. Example:

```json
[
  {
    "id": "StateGraph",
    "name": "LangGraph StateGraph",
    "keywords": ["StateGraph", "add_edge", "State"],
    "prerequisites": []
  },
  {
    "id": "Nodes",
    "name": "LangGraph Nodes",
    "keywords": ["Node", "invoke", "flow"],
    "prerequisites": ["StateGraph"]
  }
]
```

---

## 🧠 Tech Stack

- Python 3.11+
- LangChain + LangGraph
- OpenAI (GPT-3.5 / GPT-4)
- FAISS
- Pydantic
- Gradio

---

## 📈 Roadmap

- [x] Learn and review flows with RAG
- [x] Question logging + progress tracking
- [x] Gradio web interface
- [ ] Visual dashboard
- [ ] Intelligent follow-up questions
- [ ] Curriculum auto-extraction

---

## 👨‍💻 Maintained By

**Reese Ludwick**  
_Computer Science @ Shepherd University_  
_Machine Learning • LangGraph • Agentic Workflows_

---

## 📄 License

MIT License

