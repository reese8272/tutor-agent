"""Command‑line interface for interacting with the tutor agent."""

import asyncio
from agents.tutor_agent import define_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers
from dotenv import load_dotenv


# Load environment variables early so API keys are available
load_dotenv(override=True)


async def run_cli() -> None:
    """Run an interactive command‑line tutoring session."""
    # Initialize log files if they don't exist
    import json
    from pathlib import Path
    
    log_files = [Path("logs/answers_log.json"), Path("logs/question_log.json")]
    for log_file in log_files:
        log_file.parent.mkdir(exist_ok=True)
        if not log_file.exists():
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    graph = await define_graph()
    print("🧠 Welcome to the LangGraph Tutor Agent!")
    print("You can enter 'learn' to study new concepts or 'review' to test past ones.\n")

    def print_separator() -> None:
        print("=" * 60)

    # Get the initial topic and mode ONCE
    concept_input = input("What do you want to learn or review today? → ").strip()
    if concept_input.lower() in {"exit", "quit"}:
        print("👋 Exiting...")
        return

    mode = input("Choose mode ('learn' or 'review'): ").strip().lower()
    if mode not in {"learn", "review"}:
        print("❌ Invalid mode. Defaulting to 'learn'.")
        mode = "learn"

    # Create initial state as dict (LangGraph works with dicts)
    state = {
        "mode": mode,
        "target_concept_id": concept_input,
        "user_input": concept_input,
        "questions": [],
        "current_question": None,
        "user_responses": [],
        "last_feedback": None,
        "last_correct": False,
        "memory": [],
        "messages": [],
        "pending_embeddings": [],
        "retrieved_chunks": None,
        "covered_concepts": [],
        "next_suggestion": None,
    }

    # Invoke the graph to retrieve context and/or sample past questions
    result = await graph.ainvoke(state)

    # If no questions were generated, inform the user and exit
    if not result.get("questions"):
        print("⚠️ No questions generated. Try a different topic or check your docs.")
        return

    print_separator()
    print(f"[🗣️] Learning session started for: {concept_input}")
    print("Type 'stop', 'exit', or 'quit' at any time to end the session.")
    print_separator()

    # Main learning loop - continues until user says stop
    question_index = 0
    while question_index < len(result["questions"]):
        question = result["questions"][question_index]
        result["current_question"] = question
        
        correct = False
        attempts = 0
        max_attempts = 3
        
        while not correct and attempts < max_attempts:
            print(f"\nQ: {question.text}")
            user_answer = input("Your Answer: ").strip()
            
            # Check for exit commands
            if user_answer.lower() in {"stop", "exit", "quit"}:
                print("👋 Ending learning session...")
                break
                
            if not user_answer:
                print("⚠️ You must enter an answer to continue.\n")
                continue
            
            attempts += 1
            
            # Update user input and get feedback
            result["user_input"] = user_answer
            result["last_feedback"] = None
            result["last_correct"] = False
            
            # Generate feedback directly using state object
            from agents.nodes.generate_feedback_node import generate_feedback
            state_obj = TutorAgentState(**result)
            state_obj = await generate_feedback(state_obj)
            result.update(state_obj.model_dump())
            
            feedback = result.get("last_feedback", "[No feedback received]")
            print(f"\n🧠 Feedback: {feedback}\n")
            
            correct = result.get("last_correct", False)
            
            if correct:
                print("✅ Great! Let's continue building on this understanding.\n")
                # Store the correct answer
                from agents.nodes.store_answers_node import store_answer
                state_obj = TutorAgentState(**result)
                state_obj = await store_answer(state_obj)
                result.update(state_obj.model_dump())
                
            elif attempts < max_attempts:
                print("💭 Let me ask this in a different way or give you a hint...\n")
                
            else:
                print("💡 No worries! Let's build on what you do know and continue learning.")
                if result.get("retrieved_chunks"):
                    context = result["retrieved_chunks"][0][:300] + "..."
                    print(f"📖 Here's some context: {context}")
                print("✅ Let's move forward with your learning journey.\n")
                correct = True
                
                # Store the answer for learning purposes
                from agents.nodes.store_answers_node import store_answer
                state_obj = TutorAgentState(**result)
                state_obj = await store_answer(state_obj)
                result.update(state_obj.model_dump())
        
        # Check if user wants to exit
        if user_answer.lower() in {"stop", "exit", "quit"}:
            break
            
        question_index += 1
        
        # After each question, ask if they want to continue or if they have questions
        if question_index < len(result["questions"]):
            continue_input = input("Ready for the next question? (press Enter to continue, or type 'stop' to end): ").strip()
            if continue_input.lower() in {"stop", "exit", "quit"}:
                print("👋 Great learning session!")
                break

    # Session complete
    print("\n🎉 Learning session complete!")
    
    # Get next suggestion
    from agents.nodes.suggest_next_node import suggest_next_unseen_concept
    state_obj = TutorAgentState(**result)
    state_obj = await suggest_next_unseen_concept(state_obj)
    result.update(state_obj.model_dump())
    
    if result.get("next_suggestion"):
        print(f"👉 Suggested next concept to explore: {result['next_suggestion']}")
        
    # If there are any correct answers queued for embedding, process them
    if result.get("pending_embeddings"):
        print("📎 Saving your learning progress...")
        embed_and_store_user_answers(result["pending_embeddings"])
        result["pending_embeddings"] = []
        print("✅ Your learning progress has been saved!")
    
    print_separator()
    print("Thanks for learning with the LangGraph Tutor Agent! 🚀")

if __name__ == "__main__":
    asyncio.run(run_cli())