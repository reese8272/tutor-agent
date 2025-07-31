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

async def generate_concept_and_code_questions(state: TutorAgentState) -> TutorAgentState:
    print("[🧠] Generating questions from retrieved chunks...")

    if not state.retrieved_chunks:
        raise ValueError("No documentation chunks provided.")

    filtered_chunks = [
        chunk for chunk in state.retrieved_chunks
        if len(chunk.strip()) > 80 and not chunk.strip().startswith(("-", "|", "#"))
    ]

    context_str = "\n\n".join(filtered_chunks[:4])  # Take top 4 meaningful chunks

    print("[📝] Context being passed to LLM:")
    print(context_str[:1000])

    if not context_str or len(context_str) < 100:
        fallback_question = f"What is the purpose of '{state.target_concept_id}' in LangChain?"
        state.questions = [ConceptQuestion(concept_id=state.target_concept_id, text=fallback_question)]
        return state

    prompt_messages = PROMPT_TEMPLATE.format_messages(context=context_str)
    llm = ChatOpenAI(temperature=0.3)
    response = await llm.ainvoke(prompt_messages)
    raw_output = response.content.strip()

    state.questions = [
        ConceptQuestion(concept_id=state.target_concept_id, text=q.strip("- ").strip())
        for q in raw_output.split("\n") if q.strip()
    ]

    return state