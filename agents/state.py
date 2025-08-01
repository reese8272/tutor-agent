from typing import List, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from agents.types import ConceptQuestion
from langgraph.graph.message import add_messages
from operator import add


class TutorAgentState(BaseModel):
    """Represents the mutable state carried through the tutor agent.

    We use Pydantic to validate the shape of the state when it enters a LangGraph
    node. Important: LangGraph will validate inputs against this schema but
    returns a plain dictionary when nodes are executed. In order to avoid
    inadvertent sharing of mutable objects across state instances, all list
    fields should use ``default_factory`` rather than a bare list.  Additional
    fields can be added here to capture per-session data, such as a history
    of user responses.
    """

    # Which mode the agent is executing in. Determines the first node to visit
    # after leaving the router. Valid values are ``"learn"`` or ``"review"``.
    mode: Optional[str] = None
    # The concept ID the user wishes to learn about. Used when generating
    # questions and retrieving documentation.
    target_concept_id: Optional[str] = None
    # A list of generated questions for the current concept. Each item is
    # represented as a ``ConceptQuestion`` model.
    questions: Annotated[List[ConceptQuestion], add] = Field(default_factory=list)
    # The question currently being asked/answered.
    current_question: Optional[ConceptQuestion] = None
    # The raw user input (their most recent answer or concept request).
    user_input: Optional[str] = None
    # Aggregated list of user responses to past questions. This is used to
    # provide context back to an LLM or store answers to logs.
    user_responses: Annotated[List[Dict[str, str]], add] = Field(default_factory=list)
    # The most recent feedback returned by the feedback node.
    last_feedback: Optional[str] = None
    # Whether the last answer was deemed correct. Defaults to ``False``.
    last_correct: bool = False
    # Memory for chain-of-thought or summarised interactions (unused for now).
    memory: Annotated[List[Dict[str, Any]], add] = Field(default_factory=list)
    # Message history in ChatML format. Useful when exposing state to a chat UI.
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    # A list of answer logs awaiting embedding into the vector store. Each entry
    # contains the question, answer, concept_id and associated metadata.
    pending_embeddings: Annotated[List[Dict[str, Any]], add] = Field(default_factory=list)
    # Documentation chunks retrieved from the vector store for question generation.
    retrieved_chunks: Optional[List[str]] = None
    # List of concept IDs the user has already covered. Used when suggesting the
    # next concept.
    covered_concepts: Annotated[List[str], add] = Field(default_factory=list)
    # A suggested next concept for the learner to explore. Set by the
    # ``suggest_next_unseen_concept`` node.
    next_suggestion: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True
    }