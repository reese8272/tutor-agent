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

def build_tutor_agent_graph():
    graph = StateGraph(TutorAgentState)

    graph.add_node("retrieve_docs", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)
    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)

    graph.set_entry_point("retrieve_docs")

    graph.add_edge("retrieve_docs", "generate_questions")
    graph.add_edge("generate_questions", "feedback")
    graph.add_edge("feedback", "store")
    graph.add_edge("store", "suggest_next")
    graph.add_edge("suggest_next", END)

    return graph.compile()

def build_mode_routing_graph():
    graph = StateGraph(TutorAgentState)

    def entry_passthrough(state: TutorAgentState):
        return state

    graph.add_node("entry", entry_passthrough)

    graph.add_node("feedback", generate_feedback)
    graph.add_node("store", store_answer)
    graph.add_node("suggest_next", suggest_next_unseen_concept)

    graph.add_node("retrieve_docs", retrieve_context_from_docs)
    graph.add_node("generate_questions", generate_concept_and_code_questions)
    graph.add_node("review", suggest_review_questions)

    def route_mode(state: TutorAgentState):
        return "retrieve_docs" if state.mode == "learn" else "review"

    graph.add_conditional_edges(
        "entry",
        route_mode,
        {"retrieve_docs": "retrieve_docs", "review": "review"}
    )

    graph.set_entry_point("entry")

    graph.add_edge("retrieve_docs", "generate_questions")
    graph.add_edge("generate_questions", "feedback")
    graph.add_edge("review", "feedback")
    graph.add_edge("feedback", "store")
    graph.add_edge("store", "suggest_next")
    graph.add_edge("suggest_next", END)

    return graph.compile()

create_tutor_graph = build_mode_routing_graph