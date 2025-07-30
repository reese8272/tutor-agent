from agents.state import TutorAgentState


def conduct_chat_interaction(state: TutorAgentState) -> TutorAgentState:
    """Ask the user the generated questions, collect their responses."""

    print("[🗣️] Entering interactive Q&A session...")

    questions = state.current_question
    responses = []

    if not questions:
        raise ValueError("No questions to ask in state.")

    print("\n📚 Let's go through the questions. Answer each one thoughtfully.\n")

    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question}")
        answer = input("Your Answer: ").strip()
        responses.append(answer)
        print("")  # spacing

    return state.model_copy(update={"user_responses": responses})
