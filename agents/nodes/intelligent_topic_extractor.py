"""
Intelligent topic extraction agent that analyzes loaded documentation
to discover and extract all main topics from LangChain and LangGraph.
"""
import json
import pickle
from pathlib import Path
from typing import List, Dict, Set
from agents.state import TutorAgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


async def extract_topics_from_docs(state: TutorAgentState) -> TutorAgentState:
    """
    Analyze the loaded documentation to extract comprehensive topics.
    This replaces the limited static concepts.json with dynamic analysis.
    """
    
    # Check if we have loaded documentation
    raw_docs_path = Path("data/raw_docs.pkl")
    if not raw_docs_path.exists():
        state.messages.append("No loaded documentation found. Please run doc preparation first.")
        state.topics = []
        return state
    
    # Load the documentation
    with open(raw_docs_path, "rb") as f:
        docs = pickle.load(f)
    
    print(f"📚 Analyzing {len(docs)} documentation chunks for topics...")
    
    # Sample representative chunks from the documentation
    sample_size = min(50, len(docs))  # Analyze up to 50 chunks to avoid token limits
    import random
    sample_docs = random.sample(docs, sample_size)
    
    # Combine sample content for analysis
    sample_content = "\n\n".join([
        f"=== Document {i+1} ===\n{doc.page_content[:500]}" 
        for i, doc in enumerate(sample_docs[:20])  # Limit to avoid token overflow
    ])
    
    # Create prompt for topic extraction
    topic_extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at analyzing technical documentation to extract main topics and concepts.

Analyze the provided LangChain and LangGraph documentation samples and extract the main topics that users would want to learn about.

For each topic you identify, provide:
1. A clear, descriptive name
2. Whether it's a LangChain or LangGraph concept
3. A brief description of what it covers

Focus on:
- Core concepts and components
- Important classes and functions
- Key workflows and patterns
- Integration points
- Advanced features

Return your analysis as a JSON list with this structure:
[
  {
    "id": "category.topic_name",
    "name": "Human Readable Topic Name", 
    "category": "LangChain" or "LangGraph",
    "description": "Brief description of what this topic covers",
    "keywords": ["key", "terms", "related", "to", "topic"]
  }
]

Aim for 15-25 comprehensive topics that cover the breadth of LangChain and LangGraph capabilities."""),
        ("user", f"Please analyze this documentation and extract the main topics:\n\n{sample_content}")
    ])
    
    # Use GPT-4 for intelligent topic extraction
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    
    try:
        response = await llm.ainvoke(topic_extraction_prompt.format_messages())
        
        # Parse the JSON response
        topics_text = response.content.strip()
        if topics_text.startswith("```json"):
            topics_text = topics_text[7:-3].strip()
        elif topics_text.startswith("```"):
            topics_text = topics_text[3:-3].strip()
            
        topics = json.loads(topics_text)
        
        # Filter and validate topics
        validated_topics = []
        seen_ids = set()
        
        for topic in topics:
            if (isinstance(topic, dict) and 
                "id" in topic and "name" in topic and "category" in topic and
                topic["category"] in ["LangChain", "LangGraph"] and
                topic["id"] not in seen_ids):
                
                validated_topics.append({
                    "id": topic["id"],
                    "name": topic["name"],
                    "category": topic["category"],
                    "description": topic.get("description", ""),
                    "keywords": topic.get("keywords", [])
                })
                seen_ids.add(topic["id"])
        
        print(f"✅ Extracted {len(validated_topics)} topics from documentation")
        state.topics = validated_topics
        
        # Optionally save the extracted topics for future use
        extracted_topics_path = Path("data/extracted_topics.json")
        with open(extracted_topics_path, "w", encoding="utf-8") as f:
            json.dump(validated_topics, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved extracted topics to {extracted_topics_path}")
        
    except Exception as e:
        print(f"❌ Error extracting topics: {e}")
        # Fall back to the static concepts if extraction fails
        concepts_path = Path("data/concepts.json")
        if concepts_path.exists():
            with open(concepts_path, "r", encoding="utf-8") as f:
                concepts = json.load(f)
            state.topics = [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "category": c["category"]
                }
                for c in concepts if c["category"] in ("LangChain", "LangGraph")
            ]
        else:
            state.topics = []
    
    return state


async def get_cached_or_extract_topics(state: TutorAgentState) -> TutorAgentState:
    """
    Get topics from cache if available, otherwise extract from documentation.
    This provides a faster experience for repeated runs.
    """
    
    # Check for cached extracted topics first
    extracted_topics_path = Path("data/extracted_topics.json")
    
    if extracted_topics_path.exists():
        try:
            with open(extracted_topics_path, "r", encoding="utf-8") as f:
                cached_topics = json.load(f)
            
            print(f"📋 Using cached topics ({len(cached_topics)} topics found)")
            state.topics = cached_topics
            return state
            
        except Exception as e:
            print(f"⚠️ Error reading cached topics: {e}")
    
    # If no cache or error, extract from documentation
    print("🔍 No cached topics found, analyzing documentation...")
    return await extract_topics_from_docs(state)
