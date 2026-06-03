import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import simple_chat
from Search.serp_search import search_with_sources
import json
import os
def research_interviews(
    company_name: str,
    role_title: str
):
    """
    Research interview experiences and questions for a role
    
    Returns:
        tuple: (interview_data dict, sources list)
    """
    # Load sources
    sources_path = Path(__file__).parent / "job_sources.json"
    with open(sources_path, "r", encoding="utf-8") as f:
        job_sources = json.load(f)
    
    interview_sources = job_sources.get("interview_sources", [])
    
    # Gather real-time context
    print("  [LLM] Gathering real-world interview context...")
    base_query = f"{company_name} {role_title} interview experience"
    search_context = search_with_sources(base_query, interview_sources, max_results_per_source=3)
    
    if not search_context.strip():
        search_context = "No specific real-world interview experiences found. Provide general industry standard insights."

    prompt = f"""
Research interview experiences for:
Company: {company_name}
Role: {role_title}

Use the following real-world search snippets to ground your answer and prevent hallucinations:
--- SEARCH CONTEXT ---
{search_context}
--- END SEARCH CONTEXT ---

Provide common interview questions, formats, and experiences shared by candidates.
Format the response with:
1. Common Question Types
2. Interview Format
3. Difficulty Level
4. Time Complexity Focus
    """
    
    # Get research from LLM
    research_content = simple_chat(prompt)
    
    interview_data = {
        "company_name": company_name,
        "role_title": role_title,
        "interview_content": research_content,
        "sources": interview_sources
    }
    
    return interview_data, interview_sources
