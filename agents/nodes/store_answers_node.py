"""Node responsible for persisting user answers and feedback."""

import json
from datetime import datetime
from pathlib import Path
from agents.state import TutorAgentState


# Define log file paths and ensure their parent directory exists
LOG_FILE = Path("logs/answers_log.json")
QUESTION_LOG = Path("logs/question_log.json")
LOG_FILE.parent.mkdir(exist_ok=True)


async def store_answer(state: TutorAgentState) -> TutorAgentState:
    """Store the user's answer and feedback into persistent logs.

    This function appends the current question, the user's answer, and the
    feedback to ``logs/question_log.json`` on every invocation. If the answer
    was correct (as determined by ``state.last_correct``) it also appends the
    entry to ``logs/answers_log.json`` and adds the entry to
    ``state.pending_embeddings`` for later embedding. Incorrect answers are
    logged only in the question log.

    Parameters
    ----------
    state : TutorAgentState
        The current agent state containing ``current_question``, ``user_input``,
        ``last_feedback``, and ``last_correct``.

    Returns
    -------
    TutorAgentState
        The updated state with ``pending_embeddings`` possibly extended.
    """
    # If there's no current question we have nothing to store
    if not state.current_question:
        return state

    question = state.current_question
    answer = state.user_input
    feedback = state.last_feedback
    is_correct = state.last_correct

    # Build the log entry
    question_log_entry = {
        "question": question.text,
        "answer": answer,
        "concept_id": question.concept_id,
        "timestamp": datetime.now().isoformat(),
        "correct": is_correct,
        "feedback": feedback,
    }

    # Append to the question log (all answers) with proper error handling
    try:
        if QUESTION_LOG.exists() and QUESTION_LOG.stat().st_size > 0:
            with open(QUESTION_LOG, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    print("[⚠️] Question log corrupted, starting fresh")
                    logs = []
        else:
            logs = []
        logs.append(question_log_entry)
        with open(QUESTION_LOG, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[⚠️] Failed to log to question log: {e}")

    # If the answer was incorrect, we don't record it for embedding
    if not is_correct:
        print(f"❌ Answer not stored in final log (incorrect): {answer}")
        return state

    # Append to the answers log (only correct answers) and queue for embedding
    try:
        if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    print("[⚠️] Answer log corrupted, starting fresh")
                    logs = []
        else:
            logs = []
        logs.append(question_log_entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        # Add to pending embeddings queue
        state.pending_embeddings.append(question_log_entry)
        print(f"[✅] Stored correct answer: {answer}")
    except Exception as e:
        print(f"[⚠️] Failed to store answer: {e}")
    return state


# Alias used when adding this node to a graph
node = store_answer


def embed_and_store_user_answers(answer_logs):
    """Embed and store user answers using the embed_utils tool."""
    if not answer_logs:
        return
        
    try:
        from tools.embed_utils import embed_texts_and_save
        texts = [entry["answer"] for entry in answer_logs]
        metadatas = [
            {"concept_id": entry["concept_id"], "question": entry["question"]}
            for entry in answer_logs
        ]
        embed_texts_and_save(texts, metadatas, namespace="user_answers")
        print(f"[✅] Embedded and saved {len(answer_logs)} correct answers to embeddings/user_answers")
    except Exception as e:
        print(f"[⚠️] Failed to embed answers: {e}")