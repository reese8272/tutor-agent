# agents/nodes/review_node.py

import json
import random
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from prompts.review_prompt import REVIEW_PROMPT
from dotenv import load_dotenv
load_dotenv(override=True)
LOG_PATH = "logs/question_log.json"

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", REVIEW_PROMPT)
])

def suggest_review_questions(state: TutorAgentState) -> TutorAgentState:
    print("[🔁] Generating review questions...")

    # Load recent questions
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    except FileNotFoundError:
        return state.copy(update={"current_questions": ["No past questions to review."]})

    # Grab a random sample of 3 past questions
    seen_qs = [entry["question"] for entry in log_data][-20:]
    sample = random.sample(seen_qs, min(3, len(seen_qs)))

    joined_sample = "\n".join(sample)
    prompt = PROMPT_TEMPLATE.format_messages(seen_questions=joined_sample)

    llm = ChatOpenAI(temperature=0.3)
    result = llm(prompt)

    raw = result.content.strip()
    questions = [q.strip("- ").strip() for q in raw.split("\n") if q.strip()]

    return state.model_copy(update={"current_questions": questions})
