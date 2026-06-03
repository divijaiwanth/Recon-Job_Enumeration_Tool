import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import (
    simple_chat
)

from Job_Specific.prompts import (
    MISSION_ALIGNMENT_PROMPT
)


def generate_mission_alignment(
    mission: str,
    role_title: str,
    responsibilities: list[str]
):

    prompt = f"""
{MISSION_ALIGNMENT_PROMPT}

MISSION:
{mission}

ROLE:
{role_title}

RESPONSIBILITIES:

{chr(10).join(responsibilities)}
"""

    return simple_chat(
        prompt
    )