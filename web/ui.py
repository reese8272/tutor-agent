"""Gradio UI for the LangGraph Tutor Agent."""

import gradio as gr
from dotenv import load_dotenv
import asyncio
from agents.tutor_agent import define_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers


load_dotenv(override=True)


def state_to_messages(state: TutorAgentState) -> list:
    """Convert the internal tutor state into a chat message history."""
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


async def chat(user_input: str, history: list):
    """Handle a single round of chat interaction in the UI.

    On the first call, the user input is treated as the concept to learn. On
    subsequent calls it is treated as an answer to the current question. The
    agent state is maintained on the ``chat`` function itself.
    """
    # Initialise the graph once
    if not chat.graph:
        chat.graph = await define_graph()
    # If this is the first message of the session, set up a new state
    if not chat.session_state:
        chat.session_state = TutorAgentState(
            mode="learn",
            target_concept_id=user_input,
            user_input=user_input
        )
        # Run the graph to get initial questions
        chat.session_state = await chat.graph.ainvoke(chat.session_state)
        
        # Set the first question as current if available
        if chat.session_state.questions:
            chat.session_state.current_question = chat.session_state.questions[0]
    else:
        # Otherwise treat the input as an answer to the current question
        chat.session_state.user_input = user_input
        
        # Generate feedback
        from agents.nodes.generate_feedback_node import generate_feedback
        chat.session_state = await generate_feedback(chat.session_state)
        
        # Store the answer if correct
        if chat.session_state.last_correct:
            from agents.nodes.store_answers_node import store_answer
            chat.session_state = await store_answer(chat.session_state)
            
            # Move to next question if available
            if chat.session_state.questions:
                # Find current question index and move to next
                current_idx = 0
                for i, q in enumerate(chat.session_state.questions):
                    if q == chat.session_state.current_question:
                        current_idx = i
                        break
                
                if current_idx + 1 < len(chat.session_state.questions):
                    chat.session_state.current_question = chat.session_state.questions[current_idx + 1]
                else:
                    # No more questions, get next suggestion
                    from agents.nodes.suggest_next_node import suggest_next_unseen_concept
                    chat.session_state = await suggest_next_unseen_concept(chat.session_state)
                    chat.session_state.current_question = None
            
    return state_to_messages(chat.session_state)


chat.graph = None  # type: ignore[attr-defined]
chat.session_state = None  # type: ignore[attr-defined]


# Instantiate the Gradio chat interface
demo = gr.ChatInterface(
    fn=chat,
    title="LangGraph Tutor Agent",
    description="Learn or review concepts interactively!",
    submit_btn="Submit",
)


if __name__ == "__main__":
    # Launch the Gradio interface
    demo.launch()