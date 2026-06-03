import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import (
    simple_chat
)


def research_interviews(
    company_name: str,
    role_title: str
):
    """
    Research interview experiences and questions for a role
    
    Returns:
        tuple: (interview_data dict, sources list)
    """
    
    prompt = f"""
Research interview experiences for:
Company: {company_name}
Role: {role_title}

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
        "sources": [
            "LeetCode",
            "Glassdoor",
            "Reddit",
            "GitHub"
        ]
    }
    
    sources = interview_data["sources"]
    
    return interview_data, sources
