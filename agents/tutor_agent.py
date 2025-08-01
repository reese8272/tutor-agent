"""Definition of the LangGraph tutor agent."""

from langgraph.graph import StateGraph, END
from agents.state import TutorAgentState

# Shared nodes
from agents.nodes.store_answers_node import store_answer
from agents.nodes.suggest_next_node import suggest_next_unseen_concept
from agents.nodes.generate_feedback_node import generate_feedback

# Learn mode nodes
from agents.nodes.read_docs_node import retrieve_context_from_docs
from agents.nodes.generate_questions import generate_concept_and_code_questions

# Review mode node
from agents.nodes.review_node import suggest_review_questions

from agents.router import tutor_router


async def define_graph() -> StateGraph:
    """Construct and compile the tutor agent's state graph."""
    graph = StateGraph(TutorAgentState)

    # Register nodes
    graph.add_node("learn", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)
    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)
    graph.add_node("review", suggest_review_questions)
    graph.add_node("router", tutor_router)

    # Define the entry point
    graph.set_entry_point("router")

    # Define transitions for the learn path
    graph.add_edge("learn", "generate_questions")
    graph.add_edge("generate_questions", END)

    # Define transitions for the review path  
    graph.add_edge("review", END)

    return graph.compile()