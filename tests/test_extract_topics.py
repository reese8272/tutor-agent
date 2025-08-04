"""Test script for the extract main topics functionality."""
import asyncio
from agents.tutor_agent import define_graph
from agents.state import TutorAgentState


async def test_extract_topics():
    """Test that the extract_main_topics node works correctly."""
    # Test the extract_topics node directly
    print("🧪 Testing extract_main_topics node...")
    
    # Import and call the node function directly
    from agents.nodes.extract_topics_node import extract_main_topics
    
    # Create initial state object
    state = TutorAgentState(mode="extract_topics")
    
    # Run the extract_topics node directly
    result = await extract_main_topics(state)
    
    topics = result.topics
    print(f"✅ Found {len(topics)} topics:")
    
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic['name']} [{topic['category']}] (id: {topic['id']})")
    
    # Verify only LangChain and LangGraph topics are included
    categories = {topic["category"] for topic in topics}
    expected_categories = {"LangChain", "LangGraph"}
    
    if categories == expected_categories:
        print("✅ All topics are from LangChain or LangGraph categories!")
    else:
        print(f"❌ Unexpected categories found: {categories}")
        print(f"   Expected: {expected_categories}")
    
    return topics


if __name__ == "__main__":
    topics = asyncio.run(test_extract_topics())
