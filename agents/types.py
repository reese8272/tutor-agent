# agents/types.py

from pydantic import BaseModel

class ConceptQuestion(BaseModel):
    concept_id: str
    text: str
