### FILE: generate_feedback_node.py
from agents.state import TutorAgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.feedback_prompt import FEEDBACK_PROMPT
from dotenv import load_dotenv

load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_messages(FEEDBACK_PROMPT)

async def generate_feedback(state: TutorAgentState) -> TutorAgentState:
    if not state.current_question:
        return state

    question = state.current_question.text
    user_answer = state.user_input

    try:
        result = await llm.ainvoke(prompt.format_messages(question=question, answer=user_answer))
        feedback_text = result.content.strip()
        correct_flag = feedback_text.lower().startswith("correct")

        state.last_feedback = feedback_text
        state.last_correct = correct_flag

    except Exception as e:
        state.last_feedback = f"[⚠️] Error generating feedback: {e}"
        state.last_correct = False

    return state