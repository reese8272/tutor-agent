# agents/nodes/generate_questions.py

from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  # use langchain_core for consistency
from agents.state import TutorAgentState
from dotenv import load_dotenv

load_dotenv(override=True)

# Prepare the prompt template for question generation
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", QUESTION_GENERATION_PROMPT),
    ("user", "{context}")
])

def generate_concept_and_code_questions(state: TutorAgentState) -> TutorAgentState:
    """Generate concept and coding questions from retrieved documentation chunks."""
    print("[🧠] Generating questions from retrieved chunks...")

    if not state.retrieved_chunks:
        raise ValueError("No documentation chunks provided.")

    context_str = "\n\n".join(state.retrieved_chunks)

    # Format the prompt with the combined context
    prompt_messages = PROMPT_TEMPLATE.format_messages(context=context_str)
    llm = ChatOpenAI(temperature=0.3)
    response = llm(prompt_messages)
    raw_output = response.content.strip()

    # Split the output by lines into a list of questions
    questions = [q.strip("- ").strip() for q in raw_output.split("\n") if q.strip()]

    return state.model_copy(update={"current_question": questions})
