import json
import re

from ollama import chat

from Utils.config import (
    OLLAMA_MODEL
)


def structured_chat(
    prompt: str,
    schema: dict
):
    """
    Chat with schema enforcement, with fallback for malformed JSON
    """

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=schema
    )

    content = response[
        "message"
    ]["content"]

    # Try direct JSON parsing first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print(f"[WARNING] Malformed JSON, attempting recovery...")
        
        # Try to extract JSON with regex
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                print(f"[WARNING] Could not recover JSON from content")
        
        # Fallback: create structure from schema
        print(f"[WARNING] Creating default response from schema")
        return _create_default_from_schema(schema)


def _create_default_from_schema(schema: dict) -> dict:
    """Create a default response structure from schema definition"""
    
    if not schema or "properties" not in schema:
        return {}
    
    result = {}
    for key, prop in schema.get("properties", {}).items():
        if prop.get("type") == "array":
            result[key] = []
        elif prop.get("type") == "object":
            result[key] = {}
        elif prop.get("type") == "string":
            result[key] = ""
        elif prop.get("type") == "number":
            result[key] = 0
        elif prop.get("type") == "boolean":
            result[key] = False
        else:
            result[key] = None
    
    return result


def simple_chat(
    prompt: str
):

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response[
        "message"
    ]["content"]