# agents/tutor_agent.py

from langgraph.graph import StateGraph, END
from agents.state import TutorAgentState

# Shared nodes
from agents.nodes.chat_node import conduct_chat_interaction
from agents.nodes.store_answers_node import store_answer
from agents.nodes.suggest_next_node import suggest_next_unseen_concept
from agents.nodes.generate_feedback_node import generate_feedback

# Learn mode nodes
from agents.nodes.read_docs_node import retrieve_context_from_docs
from agents.nodes.generate_questions import generate_concept_and_code_questions

# Review mode node
from agents.nodes.review_node import suggest_review_questions


def build_tutor_agent_graph():
    """CLI-only, learn-mode-only graph."""
    graph = StateGraph(TutorAgentState)

    # Nodes
    graph.add_node("retrieve_docs", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)
    graph.add_node("chat", conduct_chat_interaction)
    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)

    # Entry
    graph.set_entry_point("retrieve_docs")

    # Edges
    graph.add_edge("retrieve_docs", "generate_questions")
    graph.add_edge("generate_questions", "chat")
    graph.add_edge("chat", "feedback")
    graph.add_edge("feedback", "store")
    graph.add_edge("store", "suggest_next")
    graph.add_edge("suggest_next", END)

    return graph.compile()


def build_mode_routing_graph():
    graph = StateGraph(TutorAgentState)

    # Entry passthrough
    def entry_passthrough(state): return state
    graph.add_node("entry", entry_passthrough)

    # Shared nodes
    graph.add_node("chat", conduct_chat_interaction)
    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)

    # Learn path
    graph.add_node("retrieve_docs", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)

    # Review mode
    graph.add_node("review", suggest_review_questions)

    # Conditional routing
    def route_mode(state):
        return "retrieve_docs" if state.mode == "learn" else "review"

    graph.add_conditional_edges(
        "entry",
        route_mode,
        {"retrieve_docs": "retrieve_docs", "review": "review"}
    )

    # Entry point
    graph.set_entry_point("entry")

    # Learn path
    graph.add_edge("retrieve_docs", "generate_questions")
    graph.add_edge("generate_questions", "chat")

    # Review path
    graph.add_edge("review", "chat")

    # Shared tail
    graph.add_edge("chat", "feedback")
    graph.add_edge("feedback", "store")
    graph.add_edge("store", "suggest_next")
    graph.add_edge("suggest_next", END)

    return graph.compile()

create_tutor_graph = build_mode_routing_graph