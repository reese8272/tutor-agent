# web/ui.py

import gradio as gr
from agents.tutor_agent import build_mode_routing_graph
from agents.state import TutorAgentState

session_state = {}

def run_tutor_phase_1(user_input: str, mode: str):
    state = TutorAgentState(user_input=user_input, mode=mode)
    graph = build_mode_routing_graph()

    # Run up to the chat node to get questions
    state = graph.invoke(state, until="chat")
    session_state["partial_state"] = state

    questions = state.current_question or []
    return questions[:3] + [""] * (3 - len(questions))  # pad to 3 if needed

def run_tutor_phase_2(ans1, ans2, ans3):
    state = session_state.get("partial_state")
    if not state:
        return "Session state lost. Please restart.", []

    responses = [ans1, ans2, ans3]
    responses = [r.strip() for r in responses if r.strip()]
    state.user_responses = responses

    graph = build_mode_routing_graph()
    final_state = graph.invoke(state, from_node="feedback")

    feedback = final_state.feedback_output
    suggestion = final_state.next_suggestion

    combined = f"🧠 Feedback:\n{feedback or 'No feedback'}\n\n📚 Suggestion:\n{suggestion or 'No suggestion'}"
    return combined, final_state.covered_concepts or []

with gr.Blocks() as demo:
    with gr.Row():
        user_input = gr.Textbox(label="What do you want to learn or review?")
        mode = gr.Radio(["learn", "review"], label="Mode", value="learn")
        submit_btn = gr.Button("Start Session")

    with gr.Column():
        q1 = gr.Textbox(label="Q1 Answer")
        q2 = gr.Textbox(label="Q2 Answer")
        q3 = gr.Textbox(label="Q3 Answer")
        answer_btn = gr.Button("Submit Answers")

    feedback_output = gr.Markdown()
    covered_output = gr.Textbox(label="Concepts Covered")

    submit_btn.click(fn=run_tutor_phase_1, inputs=[user_input, mode], outputs=[q1, q2, q3])
    answer_btn.click(fn=run_tutor_phase_2, inputs=[q1, q2, q3], outputs=[feedback_output, covered_output])

demo.launch()
