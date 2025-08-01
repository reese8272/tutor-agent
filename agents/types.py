"""Data models used by the tutor agent."""

from pydantic import BaseModel


class ConceptQuestion(BaseModel):
    """Represents a single question tied to a concept.

    The ``concept_id`` is used to group questions and feedback together when
    logging and embedding user answers. The ``text`` field holds the actual
    question presented to the user.
    """

    concept_id: str
    text: str