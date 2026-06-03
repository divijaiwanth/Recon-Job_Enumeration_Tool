import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import simple_chat
from Job_Specific.prompts import MISSION_ALIGNMENT_PROMPT
from Search.serp_search import search_with_sources
import json
import os
from pathlib import Path


def generate_mission_alignment(
    company_name: str,
    mission: str,
    role_title: str,
    responsibilities: list[str]
):
    # Load sources
    sources_path = Path(__file__).parent / "job_sources.json"
    with open(sources_path, "r", encoding="utf-8") as f:
        job_sources = json.load(f)
        
    role_sources = job_sources.get("role_sources", [])
    
    print("  [LLM] Gathering real-world role context...")
    base_query = f"{company_name} {role_title} engineering culture values"
    search_context = search_with_sources(base_query, role_sources, max_results_per_source=2)

    prompt = f"""
{MISSION_ALIGNMENT_PROMPT}

COMPANY MISSION:
{mission}

COMPANY CULTURE CONTEXT:
{search_context}

ROLE:
{role_title}

RESPONSIBILITIES:
{chr(10).join(responsibilities)}
"""

    return simple_chat(
        prompt
    )