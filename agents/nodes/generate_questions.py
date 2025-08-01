"""Node for generating questions from retrieved documentation."""

import json
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from agents.types import ConceptQuestion
from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT


# Load environment variables
load_dotenv(override=True)

# Compile the prompt once at import time
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(QUESTION_GENERATION_PROMPT)


async def generate_concept_and_code_questions(state: TutorAgentState) -> TutorAgentState:
    """Generate concept and code questions based on retrieved documentation.

    The function concatenates up to four of the retrieved document chunks into a
    single context string, skipping chunks that are too short or likely to be
    headings. If insufficient context is available, a simple fallback question
    based on the ``target_concept_id`` is used instead.

    This function now also checks previously asked questions to avoid repetition.

    Parameters
    ----------
    state : TutorAgentState
        The current agent state containing ``retrieved_chunks`` and the target
        concept ID.

    Returns
    -------
    TutorAgentState
        The updated state with a list of ``ConceptQuestion`` objects on
        ``state.questions``.
    """
    if not state.retrieved_chunks:
        raise ValueError("No documentation chunks provided.")

    # Load previously asked questions to avoid repetition
    previously_asked = []
    question_log_path = Path("logs/question_log.json")
    if question_log_path.exists() and question_log_path.stat().st_size > 0:
        try:
            with open(question_log_path, "r", encoding="utf-8") as f:
                past_questions = json.load(f)
                # Get questions for the same concept
                previously_asked = [
                    entry["question"] for entry in past_questions
                    if entry.get("concept_id") == state.target_concept_id
                ]
        except (json.JSONDecodeError, Exception) as e:
            print(f"[⚠️] Could not load question log: {e}")

    # Filter out very short chunks or ones that look like headings
    filtered_chunks: List[str] = [
        chunk
        for chunk in state.retrieved_chunks
        if len(chunk.strip()) > 80 and not chunk.strip().startswith(("-", "|", "#"))
    ]

    context_str = "\n\n".join(filtered_chunks[:4])

    # If there is insufficient context, generate a diverse fallback question
    if not context_str or len(context_str) < 100:
        fallback_questions = [
            f"What is the purpose of '{state.target_concept_id}' in LangChain?",
            f"How do you use '{state.target_concept_id}' in practice?",
            f"What are the key features of '{state.target_concept_id}'?",
            f"Can you explain how '{state.target_concept_id}' works?",
            f"What problems does '{state.target_concept_id}' solve?"
        ]
        
        # Choose a fallback question that hasn't been asked before
        available_fallbacks = [q for q in fallback_questions if q not in previously_asked]
        if available_fallbacks:
            chosen_question = available_fallbacks[0]
        else:
            # If all fallbacks have been used, add some variation
            chosen_question = f"Can you provide more details about '{state.target_concept_id}' and its applications?"
        
        state.questions = [ConceptQuestion(concept_id=state.target_concept_id or "unknown", text=chosen_question)]
        return state

    # Format the prompt with the context and previously asked questions
    try:
        # Create an enhanced prompt that includes previously asked questions
        context_with_history = context_str
        if previously_asked:
            context_with_history += f"\n\nPreviously asked questions to avoid repeating:\n" + "\n".join(f"- {q}" for q in previously_asked[-5:])  # Show last 5
        
        prompt_messages = PROMPT_TEMPLATE.format_messages(context=context_with_history)
        llm = ChatOpenAI(temperature=0.3)
        response = await llm.ainvoke(prompt_messages)
        raw_output = response.content.strip()

        # Split the output into individual questions, stripping bullets and whitespace
        questions = []
        for q in raw_output.split("\n"):
            if q.strip():
                question_text = q.strip("- ").strip()
                # Only add questions that haven't been asked before
                if question_text not in previously_asked and question_text not in [qu.text for qu in questions]:
                    questions.append(ConceptQuestion(concept_id=state.target_concept_id or "unknown", text=question_text))
        
        # If no new questions were generated, fall back to a diverse question
        if not questions:
            fallback_questions = [
                f"What advanced features of '{state.target_concept_id}' should developers know?",
                f"How does '{state.target_concept_id}' integrate with other LangChain components?",
                f"What are some best practices when using '{state.target_concept_id}'?",
                f"Can you explain the architecture behind '{state.target_concept_id}'?",
                f"What are common use cases for '{state.target_concept_id}'?"
            ]
            
            available_fallbacks = [q for q in fallback_questions if q not in previously_asked]
            if available_fallbacks:
                chosen_question = available_fallbacks[0]
                questions = [ConceptQuestion(concept_id=state.target_concept_id or "unknown", text=chosen_question)]
        
        state.questions = questions
        
    except Exception as e:
        print(f"[⚠️] Error generating questions: {e}")
        # Use a diverse fallback that hasn't been asked
        fallback_questions = [
            f"What is the purpose of '{state.target_concept_id}' in LangChain?",
            f"How do you implement '{state.target_concept_id}' in your applications?",
            f"What makes '{state.target_concept_id}' unique in the LangChain ecosystem?"
        ]
        
        available_fallbacks = [q for q in fallback_questions if q not in previously_asked]
        if available_fallbacks:
            chosen_question = available_fallbacks[0]
        else:
            chosen_question = f"Please explain your understanding of '{state.target_concept_id}' in detail."
        
        state.questions = [ConceptQuestion(concept_id=state.target_concept_id or "unknown", text=chosen_question)]
    
    return state


# Alias used when adding this node to a graph
node = generate_concept_and_code_questions