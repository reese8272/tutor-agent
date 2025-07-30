from agents.tutor_agent import create_tutor_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers
from dotenv import load_dotenv

load_dotenv(override=True)


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

    state = TutorAgentState(
        mode=mode,
        target_concept_id=concept_input,
        user_input=concept_input,
        messages=[],
        memory=[],
        pending_embeddings=[]
    )

    state = graph.invoke(state)

    if not state["questions"]:
        print("⚠️ No questions generated. Try a different topic or check your docs.")
        continue

    print("\n[🗣️] Entering interactive Q&A session...\n")
    for question in state["questions"]:
        print(f"Q: {question.text}")
        user_answer = input("Your Answer: ").strip()

        state["user_input"] = user_answer
        state["current_question"] = question

        state = graph.invoke(state)

        feedback = state.get("last_feedback", "")
        if feedback:
            print(f"\n🧠 Feedback: {feedback}\n")

    print("✅ Session complete!")
    if state["next_suggestion"]:
        print(f"👉 Suggested next concept: {state["next_suggestion"]}")

    if state["pending_embeddings"]:
        print("💾 Embedding correct answers...")
        embed_and_store_user_answers(state["pending_embeddings"])
        state["pending_embeddings"].clear()
        print("✅ Stored and embedded your correct answers.\n")
