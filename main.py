# main.py

from agents.tutor_agent import build_mode_routing_graph
from agents.state import TutorAgentState


def main():
    print("🧠 Welcome to the LangGraph Tutor Agent!")
    print("You can enter 'learn' to study new concepts or 'review' to test past ones.\n")

    # Collect user input
    user_input = input("What do you want to learn or review today? → ").strip()
    mode = ""
    while mode not in {"learn", "review"}:
        mode = input("Choose mode ('learn' or 'review'): ").strip().lower()

    # Build routing graph
    graph = build_mode_routing_graph()

    # Create initial state
    state = TutorAgentState(user_input=user_input, mode=mode)

    # Run the flow
    final_state = graph.invoke(state)

    # Final feedback + questions
    print("\n🧠 Tutor Feedback:")
    print(final_state.tutor_output)

    print("\n📝 Questions Asked:")
    for q in final_state.current_question:
        print(f"- {q}")

    print("\n✅ Session complete. Logged to: logs/question_log.json")


if __name__ == "__main__":
    main()
