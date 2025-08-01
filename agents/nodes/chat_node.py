"""A lightweight node for recording chat interactions.

In the original repository this node attempted to prompt the user for input
inside of a LangGraph node using ``input()``. Interactive I/O inside of graph
nodes is not recommended because nodes should remain pure functions of state.
Instead this node now simply records the current question and the provided
``user_input`` into the state's ``user_responses`` list. Real interactive
loops should be handled outside of the graph (e.g. in a CLI or UI).
"""

from agents.state import TutorAgentState


async def conduct_chat_interaction(state: TutorAgentState) -> TutorAgentState:
    """Record the user's answer to the current question.

    If both ``current_question`` and ``user_input`` are present on the state,
    append a dictionary containing the question text and answer to
    ``state.user_responses``. This allows external UIs to capture a complete
    history of Q&A pairs without needing to perform side effects here.

    Parameters
    ----------
    state : TutorAgentState
        The current state of the tutor agent.

    Returns
    -------
    TutorAgentState
        The updated state with ``user_responses`` potentially extended.
    """
    if state.current_question and state.user_input:
        state.user_responses.append({
            "question": state.current_question.text,
            "answer": state.user_input,
        })
    return state

# Alias used when adding this node to a graph
node = conduct_chat_interaction