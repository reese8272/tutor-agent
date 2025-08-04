"""Node responsible for searching and finding exact documentation references."""

import json
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from agents.state import TutorAgentState
from agents.types import ConceptQuestion

# Load environment variables
load_dotenv(override=True)

# Template for documentation search prompts
DOC_SEARCH_PROMPT = [
    (
        "system",
        """
You are a documentation search assistant helping a student find exact references in LangChain/LangGraph documentation.

The student is asking about a specific concept and wants to know:
1. Where in the documentation this concept is mentioned
2. Exact quotes or sections that explain it
3. Specific file names, sections, or page references if available

Based on the retrieved documentation chunks, provide:
- Exact quotes from the documentation that relate to their query
- Specific references to where they can find more information
- Direct excerpts that answer their question

Be precise and cite exact text when possible.
        """,
    ),
    (
        "user",
        "Student query: {query}\n\nRetrieved documentation:\n{context}",
    ),
]

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(DOC_SEARCH_PROMPT)


async def search_documentation_references(state: TutorAgentState) -> TutorAgentState:
    """Search for exact documentation references for the student's query.
    
    This node performs a semantic search through the documentation and returns
    specific excerpts, quotes, and references that directly address the student's
    question about where to find information in the docs.
    
    Parameters
    ----------
    state : TutorAgentState
        The current state containing the user's documentation search query.
        
    Returns
    -------
    TutorAgentState
        Updated state with documentation search results and references.
    """
    if not state.user_input:
        state.questions = [ConceptQuestion(
            concept_id="doc_search", 
            text="What concept would you like me to help you find in the documentation?"
        )]
        return state
    
    try:
        # Load vector store for documentation search
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            "embeddings/vector_store", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Perform semantic search with more results for doc search
        search_query = f"documentation reference for {state.user_input} {state.target_concept_id or ''}"
        docs = vectorstore.similarity_search(search_query, k=8)  # More results for comprehensive search
        
        if not docs:
            state.questions = [ConceptQuestion(
                concept_id="doc_search",
                text=f"I couldn't find documentation for '{state.user_input}'. Could you try rephrasing your search query?"
            )]
            return state
        
        # Extract content and metadata
        doc_content = []
        for doc in docs:
            content = doc.page_content
            # Add metadata if available (file source, section, etc.)
            if hasattr(doc, 'metadata') and doc.metadata:
                metadata_info = ""
                if 'source' in doc.metadata:
                    metadata_info += f"Source: {doc.metadata['source']}\n"
                if 'title' in doc.metadata:
                    metadata_info += f"Section: {doc.metadata['title']}\n"
                if metadata_info:
                    content = f"{metadata_info}\nContent: {content}"
            
            doc_content.append(content)
        
        # Format context for the LLM
        context = "\n\n---\n\n".join(doc_content)
        
        # Generate documentation search response
        llm = ChatOpenAI(temperature=0.1)  # Low temperature for precise references
        prompt_messages = PROMPT_TEMPLATE.format_messages(
            query=state.user_input, 
            context=context
        )
        response = await llm.ainvoke(prompt_messages)
        
        # Create a documentation search "question" that contains the results
        doc_search_result = ConceptQuestion(
            concept_id="doc_search",
            text=f"📚 Documentation Search Results for '{state.user_input}':\n\n{response.content.strip()}"
        )
        
        state.questions = [doc_search_result]
        state.retrieved_chunks = [doc.page_content for doc in docs]
        
    except Exception as e:
        print(f"[⚠️] Error searching documentation: {e}")
        fallback_result = ConceptQuestion(
            concept_id="doc_search",
            text=f"I encountered an error searching for '{state.user_input}' in the documentation. Please try rephrasing your query or check if the documentation is available."
        )
        state.questions = [fallback_result]
    
    return state


# Alias for graph node
node = search_documentation_references
