import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import structured_chat
from Search.serp_search import search_with_sources
import json
import os

def estimate_team(
    company_name: str,
    role_title: str
):
    """Estimate team size and type for a role"""
    # Load sources
    sources_path = Path(__file__).parent / "job_sources.json"
    with open(sources_path, "r", encoding="utf-8") as f:
        job_sources = json.load(f)
        
    team_sources = job_sources.get("team_sources", [])
    
    print("  [LLM] Gathering real-world team context...")
    base_query = f"{company_name} {role_title} engineering team structure size"
    search_context = search_with_sources(base_query, team_sources, max_results_per_source=3)
    
    if not search_context.strip():
        search_context = "No specific real-world team data found. Provide general industry standard insights."

    prompt = f"""
Estimate the team size and type for:
Company: {company_name}
Role: {role_title}

Use the following real-world search snippets to ground your answer and prevent hallucinations:
--- SEARCH CONTEXT ---
{search_context}
--- END SEARCH CONTEXT ---

Based on typical company structures and the search context provided, estimate:
1. Team size (small, medium, large)
2. Team type (distributed, co-located, hybrid)
    """

    schema = {
        "type": "object",
        "properties": {
            "estimated_team_size": {
                "type": "string"
            },
            "estimated_team_type": {
                "type": "string"
            }
        }
    }

    result = structured_chat(
        prompt,
        schema
    )

    return result