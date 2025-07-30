import json
from pathlib import Path
from agents.state import TutorAgentState
from datetime import datetime

LOG_FILE = Path("logs/answers_log.json")
LOG_FILE.parent.mkdir(exist_ok=True)

def store_answer(state: TutorAgentState) -> TutorAgentState:
    question = state.current_question
    answer = state.user_input
    feedback = state.last_feedback
    is_correct = state.last_correct

    if not is_correct:
        print(f"❌ Answer not stored (incorrect): {answer}")
        return state

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "concept_id": question.concept_id,
        "question": question.text,
        "answer": answer,
        "feedback": feedback
    }

    # Append to JSON log
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

        print(f"[✅] Stored correct answer: {answer}")

        # Add to embedding queue
        state.pending_embeddings.append(log_entry)

    except Exception as e:
        print(f"[⚠️] Failed to log answer: {e}")

    return state

node = store_answer

# For use at exit in main.py or ui.py
def embed_and_store_user_answers(answer_logs):
    from tools.embed_utils import embed_texts_and_save
    texts = [entry["answer"] for entry in answer_logs]
    metadatas = [{"concept_id": entry["concept_id"], "question": entry["question"]} for entry in answer_logs]
    embed_texts_and_save(texts, metadatas, namespace="user_answers")
