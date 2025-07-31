import json
from pathlib import Path
from agents.state import TutorAgentState
from datetime import datetime

LOG_FILE = Path("logs/answers_log.json")
QUESTION_LOG = Path("logs/question_log.json")
LOG_FILE.parent.mkdir(exist_ok=True)

async def store_answer(state: TutorAgentState) -> TutorAgentState:
    if not state.current_question:
        return state
    question = state.current_question
    answer = state.user_input
    feedback = state.last_feedback
    is_correct = state.last_correct

    question_log_entry = {
        "question": question.text,
        "answer": answer,
        "concept_id": question.concept_id,
        "timestamp": datetime.now().isoformat(),
        "correct": is_correct,
        "feedback": feedback,
    }

    try:
        if QUESTION_LOG.exists():
            with open(QUESTION_LOG, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(question_log_entry)

        with open(QUESTION_LOG, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"[⚠️] Failed to log to question log: {e}")

    if not is_correct:
        print(f"❌ Answer not stored in final log (incorrect): {answer}")
        return state

    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(question_log_entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

        print(f"[✅] Stored correct answer: {answer}")
        state.pending_embeddings.append(question_log_entry)

    except Exception as e:
        print(f"[⚠️] Failed to store answer: {e}")

    return state

node = store_answer

def embed_and_store_user_answers(answer_logs):
    from tools.embed_utils import embed_texts_and_save
    texts = [entry["answer"] for entry in answer_logs]
    metadatas = [{"concept_id": entry["concept_id"], "question": entry["question"]} for entry in answer_logs]
    embed_texts_and_save(texts, metadatas, namespace="user_answers")
