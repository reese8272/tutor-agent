"""Node responsible for generating review questions from past sessions."""

import json
import random
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state import TutorAgentState
from agents.types import ConceptQuestion
from prompts.review_prompt import REVIEW_PROMPT


# Ensure environment variables (e.g. API keys) are loaded
load_dotenv(override=True)


async def suggest_review_questions(state: TutorAgentState) -> TutorAgentState:
    """Generate follow-up questions based on the user's past answers.

    This node looks at the question log stored on disk and samples up to three
    question/answer pairs from the most recent sessions. It then asks an LLM to
    generate new conceptual and practical questions that build upon those
    previous examples. If no past questions are found, the state's ``questions``
    attribute is cleared.

    Parameters
    ----------
    state : TutorAgentState
        The current state of the tutor agent.

    Returns
    -------
    TutorAgentState
        The updated state with a list of ``ConceptQuestion`` objects ready for
        review, or an empty list if no past questions exist.
    """
    log_path = Path("logs/question_log.json")
    if not log_path.exists() or log_path.stat().st_size == 0:
        print("[ℹ️] No past questions found. Please complete a learn session first.")
        state.questions = []
        return state

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                past_questions = json.load(f)
            except json.JSONDecodeError:
                print("[ℹ️] Question log is corrupted. Nothing to review yet.")
                state.questions = []
                return state
    except Exception as e:
        print(f"[⚠️] Error reading question log: {e}")
        state.questions = []
        return state

    if not past_questions:
        print("[ℹ️] Question log is empty. Nothing to review yet.")
        state.questions = []
        return state

    # Sample up to three question/answer pairs from the last 20 entries
    sampled = random.sample(past_questions[-20:], k=min(3, len(past_questions)))
    formatted_qas = "\n".join(
        f"Q: {entry['question']}\nA: {entry['answer']}" for entry in sampled
    )

    # Build the prompt from the template. The REVIEW_PROMPT expects a
    # ``seen_questions`` variable which contains previous Q/A examples.
    prompt = ChatPromptTemplate.from_messages(REVIEW_PROMPT)

    try:
        prompt_messages = prompt.format_messages(seen_questions=formatted_qas)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
        response = await llm.ainvoke(prompt_messages)
        result = response.content.strip()
        
        # Parse questions
        questions = []
        for q in result.split("\n"):
            if q.strip():
                question_text = q.strip("- ").strip()
                questions.append(ConceptQuestion(concept_id="review_mode", text=question_text))
        
        state.questions = questions
        
    except Exception as e:
        print(f"[⚠️] Failed to generate review questions: {e}")
        state.questions = []
        return state

    return state