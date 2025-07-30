# web/ui.py

import gradio as gr
import json
from agents.state import TutorAgentState
from agents.tutor_agent import build_mode_routing_graph
from dotenv import load_dotenv
load_dotenv(override=True)

# Load concept ontology
with open("data/concepts.json", "r", encoding="utf-8") as f:
    CONCEPT_CATALOG = json.load(f)

graph = build_mode_routing_graph()

# Cache the graph state between interactions
session_state = {}

def run_tutor_phase_1(message, mode):
    state = TutorAgentState(user_input=message, mode=mode)
    state = graph.invoke(state, until="chat")  # Stop after chat step

    session_state["partial_state"] = state

    questions = state.current_question
    return questions

def run_tutor_phase_2(*answers):
    state = session_state.get("partial_state")
    if not state:
        return "No prior session found.", ""

    # Update with user answers
    state = state.model_copy(update={"user_responses": list(answers)})

    # Continue the graph to END
    final_state = graph.invoke(state, from_node="feedback")

    feedback = final_state.tutor_output

    # Display covered concepts
    concept_md = "✅ **Concepts You've Covered:**\n"
    concept_md += "\n".join(f"- {c}" for c in final_state.covered_concepts)

    # Detect curriculum completion
    all_concept_ids = {c["id"] for c in CONCEPT_CATALOG}
    covered_set = set(final_state.covered_concepts)

    if covered_set >= all_concept_ids:
        concept_md += "\n\n🎓 **You've completed the full curriculum!** 🎉"

    return f"🧠 **Feedback:**\n{feedback}\n\n✅ Session complete. Logged.", concept_md


with gr.Blocks() as demo:
    gr.Markdown("# LangGraph Tutor Agent 🧠")

    with gr.Row():
        msg = gr.Textbox(label="What do you want to learn or review?")
        mode = gr.Radio(choices=["learn", "review"], value="learn", label="Mode")
        go_btn = gr.Button("Start Session")

    question_boxes = []
    for i in range(3):
        box = gr.Textbox(label=f"Answer {i+1}")
        question_boxes.append(box)

    output = gr.Markdown()
    concept_list = gr.Markdown()
    submit_btn = gr.Button("Submit Answers")

    # Button Logic
    go_btn.click(fn=run_tutor_phase_1, inputs=[msg, mode], outputs=question_boxes)
    submit_btn.click(fn=run_tutor_phase_2, inputs=question_boxes, outputs=[output, concept_list])

demo.launch()
