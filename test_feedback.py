#!/usr/bin/env python3
"""Test the improved feedback system."""

import asyncio
from agents.nodes.generate_feedback_node import generate_feedback
from agents.state import TutorAgentState
from agents.types import ConceptQuestion

async def test_feedback_improvements():
    print("🧪 Testing improved feedback system...")
    
    # Test with a LangChain-related question and answer
    test_cases = [
        {
            "question": "How do you use 'langchain' in practice?",
            "answer": "import all the necessary packages like langchain, langchain-core, and then you can use an API key to interact with an LLM to build a chain that queries, pulls from RAG (if you have one) make API calls, and then either use tools as needed, and then lastly can give you a response that you can parse and structure as needed",
            "expected": "Should be marked as correct"
        },
        {
            "question": "What is LangChain?",
            "answer": "LangChain is a Python framework for building applications with LLMs",
            "expected": "Should be marked as correct"
        },
        {
            "question": "How do you create a chain in LangChain?",
            "answer": "You can use the | operator to chain components together",
            "expected": "Should be marked as correct"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Question: {test_case['question']}")
        print(f"Answer: {test_case['answer']}")
        print(f"Expected: {test_case['expected']}")
        
        # Create test state
        state = TutorAgentState(
            mode="learn",
            target_concept_id="langchain",
            user_input=test_case["answer"],
            current_question=ConceptQuestion(
                concept_id="langchain", 
                text=test_case["question"]
            ),
            retrieved_chunks=[
                "LangChain is a framework for developing applications powered by language models. It provides modular components that can be easily combined to create chains of operations."
            ]
        )
        
        # Test feedback generation
        result = await generate_feedback(state)
        
        print(f"Feedback: {result.last_feedback}")
        print(f"Marked as correct: {result.last_correct}")
        print(f"Status: {'✅ PASS' if result.last_correct else '❌ FAIL'}")
    
    print("\n🎯 Feedback system test completed!")

if __name__ == "__main__":
    asyncio.run(test_feedback_improvements())
