"""
Node to extract main topics from the loaded concepts database.
Returns only top-level topics for LangChain and LangGraph.
"""
import json
from agents.state import TutorAgentState
from pathlib import Path

async def extract_main_topics(state: TutorAgentState) -> TutorAgentState:
    concepts_path = Path("data/concepts.json")
    if not concepts_path.exists():
        state.messages.append("No concepts database found.")
        state.topics = []
        return state
    with open(concepts_path, "r", encoding="utf-8") as f:
        concepts = json.load(f)
    # Only include LangChain and LangGraph topics
    topics = [
        {
            "id": c["id"],
            "name": c["name"],
            "category": c["category"]
        }
        for c in concepts if c["category"] in ("LangChain", "LangGraph")
    ]
    state.topics = topics
    return state
