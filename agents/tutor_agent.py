### FILE: tutor_agent.py
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

from langgraph.checkpoint.memory import MemorySaver

async def define_graph():
    graph = StateGraph(TutorAgentState)

    graph.add_node("learn", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)
    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)
    graph.add_node("review", suggest_review_questions)

    graph.add_node("router", tutor_router)
    graph.set_entry_point("router")



    graph.add_edge("learn", "generate_questions")
    graph.add_edge("generate_questions", "feedback")
    graph.add_edge("review", "feedback")
    graph.add_edge("feedback", "store")
    graph.add_edge("store", "suggest_next")
    graph.add_edge("suggest_next", END)

    return graph.compile()
