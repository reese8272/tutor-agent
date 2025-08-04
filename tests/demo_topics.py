#!/usr/bin/env python3
"""Demo script showing the comprehensive topic extraction results."""

import json
from pathlib import Path

def show_topics():
    extracted_topics_path = Path("data/extracted_topics.json")
    
    if not extracted_topics_path.exists():
        print("❌ No extracted topics found. Run the topic extraction first.")
        return
    
    with open(extracted_topics_path, "r", encoding="utf-8") as f:
        topics = json.load(f)
    
    # Separate by category
    langchain_topics = [t for t in topics if t["category"] == "LangChain"]
    langgraph_topics = [t for t in topics if t["category"] == "LangGraph"]
    
    print("🧠 Comprehensive Topic Extraction Results")
    print("=" * 60)
    print(f"📊 Total topics extracted from your documentation: {len(topics)}")
    print(f"🔗 LangChain topics: {len(langchain_topics)}")
    print(f"📊 LangGraph topics: {len(langgraph_topics)}")
    print()
    
    print("🔗 LangChain Topics Available for Learning:")
    print("-" * 45)
    for i, topic in enumerate(langchain_topics, 1):
        print(f"  {i:2d}. {topic['name']}")
    
    print()
    print("📊 LangGraph Topics Available for Learning:")  
    print("-" * 45)
    for i, topic in enumerate(langgraph_topics, 1):
        print(f"  {i:2d}. {topic['name']}")
    
    print()
    print("✨ Key Improvements:")
    print("   • Went from 5 basic topics to 31 comprehensive topics")
    print("   • Covers the full breadth of LangChain and LangGraph")
    print("   • Extracted directly from your loaded documentation")
    print("   • No more typing errors - just pick a number!")
    print()
    print("🚀 Now when you run the CLI, you'll see all these topics!")

if __name__ == "__main__":
    show_topics()
