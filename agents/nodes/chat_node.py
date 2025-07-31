### FILE: chat_node.py
from agents.state import TutorAgentState

async def conduct_chat_interaction(state: TutorAgentState) -> TutorAgentState:
    print("[🎣️] Entering interactive Q&A session...")

    questions = state.questions
    responses = []

    if not questions:
        raise ValueError("No questions to ask in state.")

    print("\n📚 Let's go through the questions. Answer each one thoughtfully.\n")

    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question.text}")
        answer = await input("Your Answer: ").strip()
        responses.append(answer)
        print("")  # spacing

    state.user_responses = responses
    return state
