from pathlib import Path
import json
import random
from agents.prompts.review_prompt import REVIEW_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state import TutorAgentState

def suggest_review_questions(state: TutorAgentState) -> TutorAgentState:
    log_path = Path("logs/question_log.json")

    if not log_path.exists():
        print("[ℹ️] No past questions found. Please complete a learn session first.")
        return state.model_copy(update={"current_question": []})

    with open(log_path, "r") as f:
        past_questions = json.load(f)

    if not past_questions:
        print("[ℹ️] Question log is empty. Nothing to review yet.")
        return state.model_copy(update={"current_question": []})

    sampled_questions = random.sample(past_questions[-20:], k=min(3, len(past_questions)))
    formatted_qas = "\n".join(
        f"Q: {entry['question']}\nA: {entry['answer']}" for entry in sampled_questions
    )

    prompt = ChatPromptTemplate.from_messages(REVIEW_PROMPT)
    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5) | StrOutputParser()

    result = chain.invoke({"examples": formatted_qas})
    questions = [q.strip("- ").strip() for q in result.split("\n") if q.strip()]

    return state.model_copy(update={"current_question": questions})
