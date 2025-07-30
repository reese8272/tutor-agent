# agents/nodes/store_answers_node.py

import json
from pathlib import Path
from datetime import datetime
from agents.state import TutorAgentState
from datetime import datetime, timezone

timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
LOG_PATH = Path(f"logs/questions_{timestamp_str}.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


with open("data/concepts.json", "r", encoding="utf-8") as f:
    CONCEPT_CATALOG = json.load(f)


def extract_concepts_from_question(question: str) -> list:
    matched = []
    q_lower = question.lower()
    for concept in CONCEPT_CATALOG:
        for kw in concept["keywords"]:
            if kw.lower() in q_lower:
                matched.append(concept["id"])
                break
    return matched



def store_user_responses(state: TutorAgentState) -> TutorAgentState:
    """Log questions and answers, update seen questions and coverage tracking."""
    print("[💾] Storing Q&A into logs...")

    questions = state.current_question
    answers = state.user_responses

    if not questions or not answers:
        raise ValueError("Cannot store empty questions or answers.")

    timestamp = datetime.utcnow().isoformat()
    entries = []

    for question, answer in zip(questions, answers):
        entry = {
            "timestamp": timestamp,
            "question": question,
            "answer": answer,
        }
        entries.append(entry)

    # Append to question_log.json
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(entries)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    print(f"[✓] Stored {len(entries)} Q&A pairs to {LOG_PATH}")

    # Update state tracking
    updated_coverage_map = state.coverage_map.copy()
    new_concepts = []

    for q in questions:
        updated_coverage_map[q] = True
        extracted = extract_concepts_from_question(q)
        new_concepts.extend([c for c in extracted if c not in state.covered_concepts])

    return state.model_copy(update={
        "seen_questions": state.seen_questions + questions,
        "coverage_map": updated_coverage_map,
        "covered_concepts": state.covered_concepts + new_concepts,
    })
