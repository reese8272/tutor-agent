#!/usr/bin/env python3
"""Simple test for intelligent topic extraction."""

import asyncio
import os
from pathlib import Path
import sys

async def test_extraction():
    print("🔧 Environment check:")
    print(f"  - OpenAI API Key: {'✅' if 'OPENAI_API_KEY' in os.environ else '❌'}")
    
    raw_docs_path = Path('data/raw_docs.pkl')
    print(f"  - Raw docs exist: {'✅' if raw_docs_path.exists() else '❌'}")
    
    if raw_docs_path.exists():
        print(f"  - Raw docs size: {raw_docs_path.stat().st_size:,} bytes")
    
    # Check cached topics
    cached_path = Path('data/extracted_topics.json')
    print(f"  - Cached topics: {'✅' if cached_path.exists() else '❌'}")
    
    # Test basic import
    try:
        from agents.nodes.intelligent_topic_extractor import get_cached_or_extract_topics
        from agents.state import TutorAgentState
        print("  - Imports: ✅")
    except Exception as e:
        print(f"  - Imports: ❌ {e}")
        return
    
    # Test topic extraction
    try:
        print("\n🚀 Testing topic extraction...")
        state = TutorAgentState(mode='extract_topics')
        result = await get_cached_or_extract_topics(state)
        
        print(f"\n✅ Success! Found {len(result.topics)} topics:")
        for i, topic in enumerate(result.topics[:8], 1):
            print(f"  {i}. {topic['name']} [{topic['category']}]")
        
        if len(result.topics) > 8:
            print(f"  ... and {len(result.topics) - 8} more topics")
            
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_extraction())
