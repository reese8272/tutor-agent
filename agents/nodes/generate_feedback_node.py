# agents/nodes/generate_feedback_node.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from prompts.feedback_prompt import FEEDBACK_PROMPT
from dotenv import load_dotenv
load_dotenv(override=True)

PROMPT_TEMPLATE = ChatPromptTemplate.from_template(FEEDBACK_PROMPT)

def generate_feedback_node(state: TutorAgentState) -> TutorAgentState:
    """Generate feedback for each user answer."""
    print("[🔍] Generating feedback for answers...")

    questions = state.current_question
    answers = state.user_responses

    if not questions or not answers:
        raise ValueError("Missing questions or answers.")

    llm = ChatOpenAI(temperature=0.2)
    feedback_outputs = []

    for question, answer in zip(questions, answers):
        prompt = PROMPT_TEMPLATE.format_messages(question=question, answer=answer)
        result = llm(prompt)
        feedback_outputs.append(f"Q: {question}\n🧠 Feedback: {result.content.strip()}\n")

    joined_feedback = "\n".join(feedback_outputs)
    return state.model_copy(update={"tutor_output": joined_feedback})
