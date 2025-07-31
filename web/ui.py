### FILE: ui.py
import gradio as gr
import uuid
import asyncio
from dotenv import load_dotenv
from agents.tutor_agent import define_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers

load_dotenv(override=True)

def state_to_messages(state: TutorAgentState) -> list:
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

async def chat(user_input, history):
    if not chat.graph:
        chat.graph = await define_graph()

    # Set up new state if first message
    if not chat.session_state:
        chat.session_state = TutorAgentState(
            mode="learn",
            target_concept_id=user_input,
            user_input=user_input,
            messages=[],
            memory=[],
            pending_embeddings=[]
        )
    else:
        chat.session_state.user_input = user_input

    chat.session_state = await chat.graph.ainvoke(chat.session_state)
    return state_to_messages(chat.session_state)

chat.graph = None
chat.session_state = None


demo = gr.ChatInterface(
    fn=chat,
    title="LangGraph Tutor Agent",
    description="Learn or review concepts interactively!",
    submit_btn="Submit"
)

if __name__ == "__main__":
    demo.launch()