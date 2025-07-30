from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

class TutorAgentState(BaseModel):
    # User's last message
    user_input: Optional[str] = None

    # Retrieved context from FAISS
    retrieved_chunks: Optional[List[str]] = None

    # The current concept/coding question being asked
    current_question: List[str] = Field(default_factory=list)

    # User responses to those questions
    user_responses: List[str] = Field(default_factory=list)

    # Final decision from agent (e.g. feedback, next topic)
    tutor_output: Optional[str] = None

    # Log of previously seen questions (for RAG tracking)
    seen_questions: List[str] = Field(default_factory=list)

    # Metadata for tracking what's been covered
    coverage_map: Dict[str, bool] = Field(default_factory=dict)

    # Covered concepts that the agent and user already went over
    covered_concepts: List[str] = Field(default_factory=list)

    # Path to vectorstore for lookup (optional if multiple sources)
    vectorstore_path: Optional[str] = "embeddings/vector_store"

    # Review mode or learn mode
    mode: Literal["learn", "review"] = "learn"

    feedback_output: Optional[str] = None

    next_suggestion: Optional[str] = None