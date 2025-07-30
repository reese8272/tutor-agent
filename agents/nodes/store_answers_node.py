from agents.state import TutorAgentState
from pathlib import Path
import json

def store_user_responses(state: TutorAgentState) -> TutorAgentState:
    log_path = Path("logs/question_log.json")
    log_path.parent.mkdir(exist_ok=True)

    questions = state.current_question or []
    answers = state.user_responses or []

    session_log = [
        {"question": q, "answer": a}
        for q, a in zip(questions, answers)
    ]

    if log_path.exists():
        with open(log_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.extend(session_log)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

    # Update concept coverage
    covered = set(state.covered_concepts or [])
    new_concepts = set()

    try:
        with open("data/concepts.json", "r") as f:
            catalog = json.load(f)
    except:
        catalog = []

    for q in questions:
        for entry in catalog:
            for kw in entry.get("keywords", []):
                if kw.lower() in q.lower():
                    if entry["id"] not in covered:
                        new_concepts.add(entry["id"])

    updated_covered = list(covered.union(new_concepts))
    return state.model_copy(update={"covered_concepts": updated_covered})
