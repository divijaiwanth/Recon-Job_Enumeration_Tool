import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.ollama_client import (
    structured_chat
)


def estimate_team(
    company_name: str,
    role_title: str
):
    """Estimate team size and type for a role"""
    
    prompt = f"""
Estimate the team size and type for:
Company: {company_name}
Role: {role_title}

Based on typical company structures, estimate:
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