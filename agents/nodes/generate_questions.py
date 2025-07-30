### FILE: generate_questions.py
from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from agents.types import ConceptQuestion
from dotenv import load_dotenv

load_dotenv(override=True)

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    QUESTION_GENERATION_PROMPT
)

def generate_concept_and_code_questions(state: TutorAgentState) -> TutorAgentState:
    print("[🧠] Generating questions from retrieved chunks...")

    if not state.retrieved_chunks:
        raise ValueError("No documentation chunks provided.")

    context_str = "\n\n".join(state.retrieved_chunks)
    prompt_messages = PROMPT_TEMPLATE.format_messages(context=context_str)
    llm = ChatOpenAI(temperature=0.3)
    response = llm(prompt_messages)
    raw_output = response.content.strip()

    questions = [
        ConceptQuestion(concept_id=state.target_concept_id, text=q.strip("- ").strip())
        for q in raw_output.split("\n") if q.strip()
    ]

    return state.model_copy(update={"questions": questions})