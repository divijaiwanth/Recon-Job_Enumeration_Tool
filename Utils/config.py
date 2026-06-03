from dotenv import load_dotenv
import os

load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL") or "phi3:latest"
SERP_API_KEY = os.getenv("SERP_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")