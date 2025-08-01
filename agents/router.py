"""Routing node for the tutor agent."""

from agents.state import TutorAgentState
from langgraph.types import Command


def tutor_router(state: TutorAgentState) -> Command:
    """Route to the next node based on the current mode.

    The router inspects ``state.mode`` and returns a ``Command`` instructing
    LangGraph to jump to the corresponding node. Valid modes are ``"learn"``
    and ``"review"``. If an unknown mode is encountered it defaults to
    ``"learn"``.

    Parameters
    ----------
    state : TutorAgentState
        The current state of the agent, which contains a ``mode`` attribute.

    Returns
    -------
    Command
        A command directing LangGraph to the next node.
    """
    return Command(goto=state.mode or "learn")