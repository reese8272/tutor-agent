"""Node that generates feedback on the user's answer."""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import TutorAgentState
from prompts.feedback_prompt import FEEDBACK_PROMPT


# Load environment variables so the OpenAI API key is picked up from .env
load_dotenv(override=True)

# Instantiate the model once at module import time. Using a fixed temperature
# encourages consistent feedback phrasing.
_llm = ChatOpenAI(model="gpt-4", temperature=0)
_prompt = ChatPromptTemplate.from_messages(FEEDBACK_PROMPT)


async def generate_feedback(state: TutorAgentState) -> TutorAgentState:
    """Evaluate the user's answer and provide constructive feedback."""
    if not state.current_question:
        return state

    question = state.current_question.text
    user_answer = state.user_input
    
    # Build context for the feedback - include retrieved documentation if available
    context_info = ""
    if state.retrieved_chunks:
        # Use the first chunk as context to help the LLM understand the topic better
        context_info = f"\nRELEVANT DOCUMENTATION CONTEXT:\n{state.retrieved_chunks[0][:500]}...\n"
    
    # Create enhanced prompt messages with context
    try:
        # Format the base prompt
        base_messages = _prompt.format_messages(question=question, answer=user_answer)
        
        # If we have context, add it to the system message
        if context_info:
            system_message = base_messages[0]
            enhanced_system_content = system_message.content + context_info
            base_messages[0].content = enhanced_system_content
        
        result = await _llm.ainvoke(base_messages)
        feedback_text = result.content.strip()
        
        # More robust correct answer detection
        correct_flag = (
            feedback_text.lower().startswith("correct") or 
            "correct!" in feedback_text.lower() or
            "your answer is correct" in feedback_text.lower() or
            "you're right" in feedback_text.lower() or
            "that's right" in feedback_text.lower() or
            "good job" in feedback_text.lower() or
            "you're on the right track!" in feedback_text.lower() or
            feedback_text.lower().startswith("you're on the right track")
        )
        
        # Update state fields directly
        state.last_feedback = feedback_text
        state.last_correct = correct_flag
        
        return state
    except Exception as e:
        state.last_feedback = f"[⚠️] Error generating feedback: {e}"
        state.last_correct = False
        return state


# Alias used when adding this node to a graph
node = generate_feedback