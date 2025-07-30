from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from agents.types import ConceptQuestion

class TutorAgentState(BaseModel):
    mode: str  # "learn" or "review"
    target_concept_id: Optional[str] = None
    questions: List[ConceptQuestion] = []
    current_question: Optional[ConceptQuestion] = None
    user_input: Optional[str] = None
    last_feedback: Optional[str] = None
    last_correct: bool = False
    memory: List[Dict[str, Any]] = []
    pending_embeddings: List[Dict[str, Any]] = []
    messages: List[BaseMessage] = []
