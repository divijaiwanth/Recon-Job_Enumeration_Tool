import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Company_Specific.Scrape_Context import scrape_page
from pydantic_models import CompanyOverview
from Utils.ollama_client import structured_chat

def analyze_company(company_name, website, company_text):
    schema = CompanyOverview.model_json_schema()
    prompt = f"""
    You are a company research analyst.
    Analyze the website content.
    Company:
    {company_name}
    Website:
    {website}
    Content:
    {company_text}
    Extract:
    1. Mission
    2. Products
    3. Recent launches
    4. Hiring signals

    The answer you give should be Interview ready for a candidate who has an interview with the company.
    The answer should be concise and to the point, with clarity and depth. 
    
    Tell you dont know if you dont know.

    Return ONLY valid JSON with these fields: company_name, website, mission, products (list), recent_launches (list), hiring_signals (list).
    """

    data = structured_chat(prompt, schema)

    return CompanyOverview(**data)


