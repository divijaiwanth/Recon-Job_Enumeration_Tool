from pydantic_models import (
    ResumeAnalysis
)

from Utils.ollama_client import (
    structured_chat
)

from Job_Specific.prompts import (
    RESUME_MATCH_PROMPT
)


def analyze_resume_match(
    resume_text: str,
    jd_text: str
):

    schema = {
        "type": "object",

        "properties": {

            "match_score": {
                "type": "number"
            },

            "matching_skills": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "missing_skills": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "recommended_projects": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },

            "resume_gaps": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }

    prompt = f"""
{RESUME_MATCH_PROMPT}

JOB DESCRIPTION

{jd_text}

-----------------

RESUME

{resume_text}
"""

    result = structured_chat(
        prompt,
        schema
    )

    return ResumeAnalysis(
        match_score=result.get(
            "match_score",
            0
        ),

        matching_skills=result.get(
            "matching_skills",
            []
        ),

        missing_skills=result.get(
            "missing_skills",
            []
        ),

        recommended_projects=result.get(
            "recommended_projects",
            []
        ),

        resume_gaps=result.get(
            "resume_gaps",
            []
        )
    )