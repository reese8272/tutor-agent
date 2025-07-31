from agents.state import TutorAgentState
from langgraph.types import Command

def tutor_router(state: TutorAgentState) -> Command:
    return Command(goto=state.mode)  # ✅ NOT just `state.mode`
