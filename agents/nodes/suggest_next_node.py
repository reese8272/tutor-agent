"""Node that suggests the next concept for the learner to explore."""

import json
from pathlib import Path
from agents.state import TutorAgentState


async def suggest_next_unseen_concept(state: TutorAgentState) -> TutorAgentState:
    """Determine an appropriate next concept that has not yet been covered.

    The ``data/concepts.json`` file defines a directed acyclic graph of concepts
    and their prerequisites. This function looks for the first concept whose
    prerequisites are all contained in ``state.covered_concepts`` and that has
    not itself been covered. The chosen concept's name is stored on
    ``state.next_suggestion``. If no such concept exists, ``next_suggestion``
    will be set to ``None``.

    Parameters
    ----------
    state : TutorAgentState
        The current agent state.

    Returns
    -------
    TutorAgentState
        The updated state with ``next_suggestion`` populated or cleared.
    """
    concepts_file = Path("data/concepts.json")
    if not concepts_file.exists():
        print("[⚠️] Missing data/concepts.json; cannot suggest next concept.")
        state.next_suggestion = None
        return state

    try:
        with open(concepts_file, "r", encoding="utf-8") as f:
            all_concepts = json.load(f)
    except Exception as e:
        print(f"[⚠️] Failed to load concepts: {e}")
        state.next_suggestion = None
        return state

    covered = set(state.covered_concepts or [])
    suggestion = None
    for concept in all_concepts:
        concept_id = concept.get("id")
        prereqs = set(concept.get("prerequisites", []))
        if concept_id not in covered and prereqs.issubset(covered):
            suggestion = concept.get("name", concept_id)
            break

    state.next_suggestion = suggestion
    return state


# Alias used when adding this node to a graph
node = suggest_next_unseen_concept