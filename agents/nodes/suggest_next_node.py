# agents/nodes/suggest_next_node.py

import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from dotenv import load_dotenv
load_dotenv(override=True)

# Load the global concept catalog
with open("data/concepts.json", "r", encoding="utf-8") as f:
    CONCEPT_CATALOG = json.load(f)

SYSTEM_PROMPT = """
You are a helpful AI tutor who tracks student progress.

The user has already covered the following concepts:
{covered_concepts}

Here are other possible concepts they have **not** seen yet:
{uncovered_concepts}

Based on the following documentation context:
{retrieved_chunks}

Suggest one or two specific **uncovered** concepts or coding ideas that the student should learn next.
Be as concrete and actionable as possible.
Only choose from the unseen concept list provided.
"""

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT)
])

def suggest_next_unseen_concept(state: TutorAgentState) -> TutorAgentState:
    """Suggest next topic based on documentation and coverage map."""

    print("[🧭] Suggesting next topic to explore...")

    # Covered + uncovered concepts
    covered_set = set(state.covered_concepts or [])
    uncovered = []
    for concept in CONCEPT_CATALOG:
        cid = concept["id"]
        prereqs = concept.get("prerequisites", [])
        if cid not in covered_set and all(p in covered_set for p in prereqs):
            uncovered.append(concept["name"])

    uncovered = sorted(uncovered)
    covered_str = "\n".join(state.covered_concepts or ["None"])
    uncovered_str = "\n".join(uncovered or ["None"])
    context_str = "\n\n".join(state.retrieved_chunks or [])

    prompt = PROMPT_TEMPLATE.format_messages(
        covered_concepts=covered_str,
        uncovered_concepts=uncovered_str,
        retrieved_chunks=context_str,
    )

    llm = ChatOpenAI(temperature=0.3)
    result = llm(prompt)
    suggestion = result.content.strip()

    return state.model_copy(update={"tutor_output": suggestion})
