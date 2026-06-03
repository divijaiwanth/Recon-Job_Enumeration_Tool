import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_models import RoleAnalysis
from Utils.ollama_client import structured_chat
from Job_Specific.prompts import JD_ANALYSIS_PROMPT


def analyze_jd(
    role_title: str,
    jd_text: str
):

    schema = {
        "type": "object",
        "properties": {

            "requirements": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "preferred_qualifications": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "responsibilities": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "competencies": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "evaluation_criteria": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }

    prompt = f"""
{JD_ANALYSIS_PROMPT}

JOB DESCRIPTION:

{jd_text}
"""

    result = structured_chat(prompt, schema)

    return RoleAnalysis(
        role_title=role_title,
        requirements=result.get("requirements", []),
        preferred_qualifications=result.get("preferred_qualifications", []),
        responsibilities=result.get("responsibilities", []),
        competencies=result.get("competencies", []),
        evaluation_criteria=result.get("evaluation_criteria", [])
    )