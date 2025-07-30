from pathlib import Path
import json
import random
from prompts.review_prompt import REVIEW_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state import TutorAgentState
from agents.types import ConceptQuestion
from dotenv import load_dotenv

load_dotenv(override=True)


def suggest_review_questions(state: TutorAgentState) -> TutorAgentState:
    log_path = Path("logs/question_log.json")

    if not log_path.exists():
        print("[ℹ️] No past questions found. Please complete a learn session first.")
        return state.model_copy(update={"questions": []})

    with open(log_path, "r") as f:
        past_questions = json.load(f)

    if not past_questions:
        print("[ℹ️] Question log is empty. Nothing to review yet.")
        return state.model_copy(update={"questions": []})

    sampled = random.sample(past_questions[-20:], k=min(3, len(past_questions)))
    formatted_qas = "\n".join(f"Q: {entry['question']}\nA: {entry['answer']}" for entry in sampled)

    prompt = ChatPromptTemplate.from_messages(REVIEW_PROMPT)
    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5) | StrOutputParser()

    result = chain.invoke({"examples": formatted_qas})
    new_qs = [ConceptQuestion(concept_id="review_mode", text=q.strip("- ").strip()) for q in result.split("\n") if q.strip()]

    return state.model_copy(update={"questions": new_qs})
