from agents.state import TutorAgentState
from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)


def suggest_next_unseen_concept(state: TutorAgentState) -> TutorAgentState:
    concepts_file = Path("data/concepts.json")
    if not concepts_file.exists():
        print("[⚠️] Missing data/concepts.json")
        return state

    with open(concepts_file, "r") as f:
        all_concepts = json.load(f)

    covered = set(state.covered_concepts or [])
    uncovered = []

    for concept in all_concepts:
        prereqs = set(concept.get("prerequisites", []))
        if concept["id"] not in covered and prereqs.issubset(covered):
            uncovered.append(concept["name"])

    context = "\n".join(state.retrieved_chunks or [])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a curriculum guide."),
        ("user", "Covered: {covered}\nUncovered: {uncovered}\nDocs: {docs}\nSuggest the next best concept to study.")
    ])
    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4) | StrOutputParser()

    result = chain.invoke({
        "covered": list(covered),
        "uncovered": uncovered,
        "docs": context[:4000]
    })

    return state.model_copy(update={"next_suggestion": result.strip()})
