"""
Quick topic extraction that analyzes file names and content patterns
to find comprehensive topics without requiring OpenAI API calls.
"""
import json
import pickle
import re
from pathlib import Path
from typing import List, Dict, Set
from agents.state import TutorAgentState


async def quick_extract_topics_from_docs(state: TutorAgentState) -> TutorAgentState:
    """
    Quickly analyze loaded documentation to extract topics based on patterns.
    This is a fast alternative that doesn't require LLM calls.
    """
    
    # Check if we have loaded documentation
    raw_docs_path = Path("data/raw_docs.pkl")
    if not raw_docs_path.exists():
        print("❌ No loaded documentation found.")
        state.topics = []
        return state
    
    # Load the documentation
    with open(raw_docs_path, "rb") as f:
        docs = pickle.load(f)
    
    print(f"📚 Analyzing {len(docs)} documentation chunks for topics...")
    
    # Pattern-based topic extraction
    langchain_topics = set()
    langgraph_topics = set()
    
    # Common LangChain patterns
    langchain_patterns = {
        'chains': 'Chains and LCEL',
        'prompt': 'Prompt Templates',
        'embedding': 'Embeddings',
        'vectorstore': 'Vector Stores',
        'retriever': 'Retrievers', 
        'agent': 'Agents',
        'tool': 'Tools',
        'memory': 'Memory',
        'callback': 'Callbacks',
        'chat_model': 'Chat Models',
        'llm': 'Language Models',
        'output_parser': 'Output Parsers',
        'document_loader': 'Document Loaders',
        'text_splitter': 'Text Splitters',
        'rag': 'RAG (Retrieval Augmented Generation)',
        'runnable': 'Runnables',
        'invoke': 'Invocation Patterns',
        'stream': 'Streaming'
    }
    
    # Common LangGraph patterns  
    langgraph_patterns = {
        'stategraph': 'StateGraph Basics',
        'add_node': 'Graph Nodes',
        'add_edge': 'Graph Edges', 
        'conditional_edge': 'Conditional Routing',
        'checkpoint': 'Checkpointing',
        'interrupt': 'Human-in-the-Loop',
        'parallel': 'Parallel Execution',
        'subgraph': 'Subgraphs',
        'compile': 'Graph Compilation',
        'workflow': 'Workflows',
        'state': 'State Management',
        'branch': 'Branching Logic'
    }
    
    # Analyze documentation content
    for doc in docs:
        content = doc.page_content.lower()
        
        # Check for LangChain topics
        for pattern, topic in langchain_patterns.items():
            if pattern in content:
                langchain_topics.add(topic)
        
        # Check for LangGraph topics  
        for pattern, topic in langgraph_patterns.items():
            if pattern in content:
                langgraph_topics.add(topic)
    
    # Also check metadata for file paths to identify more topics
    for doc in docs:
        if hasattr(doc, 'metadata') and 'source' in doc.metadata:
            source = doc.metadata['source'].lower()
            
            # Extract topics from file paths
            if 'langchain' in source:
                if 'agent' in source: langchain_topics.add('Agents')
                if 'chain' in source: langchain_topics.add('Chains and LCEL')
                if 'prompt' in source: langchain_topics.add('Prompt Engineering')
                if 'retriev' in source: langchain_topics.add('Retrievers')
                if 'embed' in source: langchain_topics.add('Embeddings')
                if 'vector' in source: langchain_topics.add('Vector Stores')
                if 'tool' in source: langchain_topics.add('Tools')
                if 'memory' in source: langchain_topics.add('Memory')
                if 'callback' in source: langchain_topics.add('Callbacks')
                
            if 'langgraph' in source:
                if 'state' in source: langgraph_topics.add('State Management')
                if 'graph' in source: langgraph_topics.add('Graph Construction')
                if 'node' in source: langgraph_topics.add('Graph Nodes')
                if 'edge' in source: langgraph_topics.add('Graph Edges')
                if 'workflow' in source: langgraph_topics.add('Workflows')
                if 'checkpoint' in source: langgraph_topics.add('Checkpointing')
    
    # Create structured topic list
    topics = []
    
    # Add LangChain topics
    for i, topic in enumerate(sorted(langchain_topics), 1):
        topics.append({
            "id": f"langchain.{topic.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')}",
            "name": topic,
            "category": "LangChain",
            "description": f"Learn about {topic} in LangChain",
            "keywords": [topic.lower()]
        })
    
    # Add LangGraph topics
    for i, topic in enumerate(sorted(langgraph_topics), 1):
        topics.append({
            "id": f"langgraph.{topic.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')}",
            "name": topic,
            "category": "LangGraph", 
            "description": f"Learn about {topic} in LangGraph",
            "keywords": [topic.lower()]
        })
    
    print(f"✅ Found {len(langchain_topics)} LangChain topics and {len(langgraph_topics)} LangGraph topics")
    
    state.topics = topics
    
    # Save the extracted topics
    extracted_topics_path = Path("data/extracted_topics.json")
    with open(extracted_topics_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(topics)} topics to {extracted_topics_path}")
    
    return state
