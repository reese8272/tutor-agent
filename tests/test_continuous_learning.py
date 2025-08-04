#!/usr/bin/env python3
"""Test the improved continuous learning flow."""

import asyncio
from agents.nodes.generate_feedback_node import generate_feedback
from agents.state import TutorAgentState
from agents.types import ConceptQuestion

async def test_continuous_learning():
    print("🧪 Testing improved continuous learning flow...")
    
    # Simulate a partially correct answer that should be encouraged
    state = TutorAgentState(
        mode="learn",
        target_concept_id="langchain",
        user_input="You use it to create chains of LLM operations",
        current_question=ConceptQuestion(
            concept_id="langchain", 
            text="How do you use LangChain in practice?"
        ),
        retrieved_chunks=[
            "LangChain is a framework for developing applications powered by language models. It provides modular components that can be easily combined to create chains of operations, integrate with vector databases, and build complex workflows."
        ]
    )
    
    # Test feedback generation
    result = await generate_feedback(state)
    
    print(f"Question: {state.current_question.text}")
    print(f"Answer: {state.user_input}")
    print(f"Feedback: {result.last_feedback}")
    print(f"Marked as correct: {result.last_correct}")
    
    # Check if it recognizes partial correctness
    if "right track" in result.last_feedback.lower() or "correct" in result.last_feedback.lower():
        print("✅ System recognizes understanding and encourages continuation")
    else:
        print("❌ System may be too strict")
    
    print("\n🎯 Continuous learning test completed!")

if __name__ == "__main__":
    asyncio.run(test_continuous_learning())
