# main.py

from agents.tutor_agent import build_mode_routing_graph
from agents.state import TutorAgentState

def main():
    print("🧠 Welcome to the LangGraph Tutor Agent!")
    print("You can enter 'learn' to study new concepts or 'review' to test past ones.\n")

    user_input = input("What do you want to learn or review today? → ")
    mode = input("Choose mode ('learn' or 'review'): ").strip().lower()

    if mode not in {"learn", "review"}:
        print("[❌] Invalid mode.")
        return

    state = TutorAgentState(user_input=user_input, mode=mode)
    graph = build_mode_routing_graph()
    final_state = graph.invoke(state)

    print("\n🧠 Tutor Feedback:\n" + (final_state.feedback_output or "[No feedback generated]"))
    print("\n📚 Suggested Next Concept:\n" + (final_state.next_suggestion or "[No suggestion]"))

    print("\n✅ Session complete. Logged to: logs/question_log.json")

if __name__ == "__main__":
    main()
