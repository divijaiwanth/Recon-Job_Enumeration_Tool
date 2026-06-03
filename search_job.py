import sys
from pathlib import Path

# Add root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from Job_Specific.JD_Analyzer import (
    analyze_jd
)

jd = """
We are looking for a Backend Engineer.

Requirements:
Python
FastAPI
Docker

Responsibilities:
Build APIs
Work with cloud infrastructure
"""

result = analyze_jd(
    "Backend Engineer",
    jd
)

print(result.model_dump())