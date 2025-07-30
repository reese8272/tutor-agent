from agents.state import TutorAgentState
from prompts.feedback_prompt import FEEDBACK_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_feedback_node(state: TutorAgentState) -> TutorAgentState:
    questions = state.current_question
    answers = state.user_responses

    if not questions or not answers:
        return state

    prompt = ChatPromptTemplate.from_messages(FEEDBACK_PROMPT)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    parser = StrOutputParser()

    feedback = ""
    for q, a in zip(questions, answers):
        qa_prompt = prompt.format_messages(question=q, answer=a)
        result = parser.invoke(llm.invoke(qa_prompt))
        feedback += f"\nQ: {q}\n🧠 Feedback: {result.strip()}\n"

    return state.model_copy(update={"feedback_output": feedback.strip()})
