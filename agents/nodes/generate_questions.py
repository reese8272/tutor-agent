# agents/nodes/generate_questions.py

from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from dotenv import load_dotenv

load_dotenv(override=True)

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", QUESTION_GENERATION_PROMPT),
    ("user", "{context}")
])

def generate_concept_and_code_questions(state: TutorAgentState) -> TutorAgentState:
    """Generate concept + practical questions from retrieved docs."""
    print("[🧠] Generating questions from retrieved chunks...")

    if not state.retrieved_chunks:
        raise ValueError("No documentation chunks provided.")

    context_str = "\n\n".join(state.retrieved_chunks)

    prompt = PROMPT_TEMPLATE.format_messages(context=context_str)
    llm = ChatOpenAI(temperature=0.3)
    response = llm(prompt)
    raw_output = response.content.strip()

    questions = [q.strip("- ").strip() for q in raw_output.split("\n") if q.strip()]

    # ✅ FIX: use the correct state field `current_question`
    return state.model_copy(update={"current_question": questions})
