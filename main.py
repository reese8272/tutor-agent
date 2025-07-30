from agents.tutor_agent import create_tutor_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers

graph = create_tutor_graph()

print("🧠 Welcome to the LangGraph Tutor Agent!")
print("You can enter 'learn' to study new concepts or 'review' to test past ones.\n")

while True:
    concept_input = input("What do you want to learn or review today? → ").strip()
    if concept_input.lower() in {"exit", "quit"}:
        print("👋 Exiting...")
        break

    mode = input("Choose mode ('learn' or 'review'): ").strip().lower()
    if mode not in {"learn", "review"}:
        print("❌ Invalid mode. Try again.")
        continue

    # Initialize state
    state = TutorAgentState(
        mode=mode,
        target_concept_id=concept_input,
        user_input="",
        messages=[],
        memory=[],
        pending_embeddings=[]
    )

    state = graph.invoke(state)

    print("\n[🗣️] Entering interactive Q&A session...\n")
    for question in state.questions:
        print(f"Q: {question.text}")
        user_answer = input("Your Answer: ").strip()

        state.user_input = user_answer
        state.current_question = question

        # Run through graph again with current answer
        state = graph.invoke(state)

        # Show feedback after each answer
        feedback = state.get("last_feedback", "")
        if feedback:
            print(f"\n🧠 Feedback: {feedback}\n")

    print("✅ Session complete! Type 'exit' to quit or start another round.")

    # Handle post-session answer embedding
    if state.pending_embeddings:
        print("💾 Embedding correct answers...")
        embed_and_store_user_answers(state.pending_embeddings)
        state.pending_embeddings.clear()
        print("✅ Stored and embedded your correct answers.\n")
