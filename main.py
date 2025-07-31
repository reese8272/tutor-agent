### FILE: main.py
import asyncio
from agents.tutor_agent import define_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers
from dotenv import load_dotenv

load_dotenv(override=True)

def state_to_messages(state) -> list:
    messages = []

    if state.target_concept_id:
        messages.append({"role": "system", "content": f"Concept: {state.target_concept_id}"})

    if state.current_question:
        messages.append({"role": "assistant", "content": f"Question: {state.current_question.text}"})

    if state.user_input:
        messages.append({"role": "user", "content": state.user_input})

    if state.last_feedback:
        messages.append({"role": "assistant", "content": f"Feedback: {state.last_feedback}"})

    if state.next_suggestion:
        messages.append({"role": "system", "content": f"Next Suggested Concept: {state.next_suggestion}"})

    return messages

async def main():
    graph = await define_graph()

    print("🧠 Welcome to the LangGraph Tutor Agent!")
    print("You can enter 'learn' to study new concepts or 'review' to test past ones.\n")

    def print_separator():
        print("=" * 60)

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

        state = await graph.ainvoke(state)

        if not state["questions"]:
            print("⚠️ No questions generated. Try a different topic or check your docs.")
            continue

        print_separator()
        print("[🗣️] Entering interactive Q&A session...")
        print_separator()

        for question in state["questions"]:
            correct = False
            state["current_question"] = question

            while not correct:
                print(f"Q: {question.text}")
                user_answer = input("Your Answer: ").strip()
                if not user_answer:
                    print("⚠️ You must enter an answer to continue.\n")
                    continue

                state["user_input"] = user_answer
                state = await graph.ainvoke(state)

                feedback = state["last_feedback"] or "[No feedback received]"
                print(f"\n🧠 Feedback: {feedback}\n")

                correct = state["last_correct"]
                if not correct:
                    print("❌ Try again.\n")

        print("\n🎉 Session complete!")
        if state["next_suggestion"]:
            print(f"👉 Suggested next concept: {state["next_suggestion"]}")

        if state["pending_embeddings"]:
            print("📎 Embedding correct answers...")
            embed_and_store_user_answers(state["pending_embeddings"])
            state["pending_embeddings"].clear()
            print("✅ Stored and embedded your correct answers.\n")

        print_separator()

if __name__ == "__main__":
    asyncio.run(main())