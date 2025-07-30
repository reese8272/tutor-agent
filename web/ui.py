import gradio as gr
from agents.tutor_agent import create_tutor_graph
from agents.state import TutorAgentState
from agents.nodes.store_answers_node import embed_and_store_user_answers
from dotenv import load_dotenv

load_dotenv(override=True)


graph = create_tutor_graph()

with gr.Blocks() as demo:
    gr.Markdown("# 🧠 LangGraph Tutor Agent (Web UI)")

    with gr.Row():
        mode_dropdown = gr.Dropdown(choices=["learn", "review"], label="Mode", value="learn")
        concept_input = gr.Textbox(label="What concept do you want to study?", placeholder="e.g., langgraph.StateGraph")
        start_button = gr.Button("Start Session")

    chat_box = gr.Chatbot(label="Tutor Chat")
    user_msg = gr.Textbox(label="Your Answer", placeholder="Type here...", interactive=False)
    submit_btn = gr.Button("Submit Answer", interactive=False)
    end_btn = gr.Button("End Session", interactive=False)
    suggestion_box = gr.Textbox(label="Next Suggested Concept", interactive=False)

    session_state = {
        "state": None,
        "question_index": 0,
        "questions": [],
        "history": [],
    }

    def start_session(concept, mode):
        session_state["state"] = TutorAgentState(
            mode=mode,
            target_concept_id=concept,
            user_input="",
            messages=[],
            memory=[],
            pending_embeddings=[]
        )
        session_state["state"] = graph.invoke(session_state["state"])
        session_state["questions"] = session_state["state"].questions
        session_state["question_index"] = 0
        session_state["history"] = []

        if not session_state["questions"]:
            return gr.update(visible=True), "⚠️ No questions generated.", gr.update(interactive=False), gr.update(interactive=False), ""

        q = session_state["questions"][0].text
        session_state["history"].append(("Tutor", q))
        return session_state["history"], "", gr.update(interactive=True), gr.update(interactive=True), ""

    def answer_question(user_input):
        idx = session_state["question_index"]
        question = session_state["questions"][idx]
        session_state["state"].user_input = user_input
        session_state["state"].current_question = question

        session_state["state"] = graph.invoke(session_state["state"])
        feedback = session_state["state"].get("last_feedback", "")

        session_state["history"].append(("You", user_input))
        session_state["history"].append(("Tutor", f"🧠 Feedback: {feedback}"))

        session_state["question_index"] += 1
        if session_state["question_index"] < len(session_state["questions"]):
            next_q = session_state["questions"][session_state["question_index"]].text
            session_state["history"].append(("Tutor", next_q))
        else:
            session_state["history"].append(("Tutor", "✅ You've completed this session. Click 'End Session' to embed your correct answers."))

        return session_state["history"], ""

    def end_session():
        suggestion = session_state["state"].next_suggestion or "No suggestion available."
        if session_state["state"].pending_embeddings:
            embed_and_store_user_answers(session_state["state"].pending_embeddings)
            session_state["state"].pending_embeddings.clear()
            session_state["history"].append(("System", "✅ Embedded all correct answers and ended session."))
        else:
            session_state["history"].append(("System", "No correct answers to embed."))
        return session_state["history"], suggestion

    start_button.click(
        start_session,
        inputs=[concept_input, mode_dropdown],
        outputs=[chat_box, user_msg, submit_btn, end_btn, suggestion_box],
    )

    submit_btn.click(
        answer_question,
        inputs=[user_msg],
        outputs=[chat_box, user_msg],
    )

    end_btn.click(
        end_session,
        outputs=[chat_box, suggestion_box]
    )

demo.launch()
