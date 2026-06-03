import sys
from pathlib import Path
from collections import Counter

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Search.serp_search import (
    search_dsa,
    search_reddit,
    search_glassdoor
)

from Search.firecrawl_search import (
    scrape_with_firecrawl
)

from Utils.ollama_client import (
    simple_chat,
    structured_chat
)

from pydantic_models import (
    RepeatedQuestion
)


MAX_PAGES = 8


def find_repeated_dsa(
    company_name: str,
    role_title: str = "Software Engineer"
):
    """
    Find repeated DSA questions for a company and role
    
    Searches multiple sources:
    - LeetCode discussions
    - Reddit interview threads
    - Glassdoor company reviews
    
    Returns:
        tuple: (analysis dict with repeated questions, source distribution)
    """
    
    print(f"\n[DSA] Searching for {company_name} {role_title} interview questions...")
    
    search_results = []
    source_counts = {}
    
    # Step 1: Search from multiple sources
    print("[DSA] Searching LeetCode...")
    leetcode_results = search_dsa(company_name)
    search_results.extend(leetcode_results)
    source_counts["LeetCode"] = len(leetcode_results)
    
    print("[DSA] Searching Reddit...")
    reddit_results = search_reddit(company_name, role_title)
    search_results.extend(reddit_results)
    source_counts["Reddit"] = len(reddit_results)
    
    print("[DSA] Searching Glassdoor...")
    glassdoor_results = search_glassdoor(company_name, role_title)
    search_results.extend(glassdoor_results)
    source_counts["Glassdoor"] = len(glassdoor_results)
    
    print(f"[DSA] Found {len(search_results)} total results")
    
    # Step 2: Extract content from top pages
    print(f"[DSA] Scraping top {min(MAX_PAGES, len(search_results))} pages...")
    page_contents = []
    
    for i, result in enumerate(search_results[:MAX_PAGES]):
        try:
            url = result.get("link", "")
            if url:
                print(f"  [{i+1}/{MAX_PAGES}] Scraping {url[:50]}...")
                content = scrape_with_firecrawl(url)
                if content:
                    markdown = content.markdown if hasattr(content, "markdown") else (content.get("markdown", "") if isinstance(content, dict) else "")
                    if markdown:
                        page_contents.append({
                            "url": url,
                            "title": result.get("title", ""),
                            "content": markdown[:2000]  # Limit content
                        })
        except Exception as e:
            print(f"  [Error scraping {url}] {str(e)}")
            continue
    
    print(f"[DSA] Successfully scraped {len(page_contents)} pages")
    
    # Step 3: Aggregate content and find patterns
    combined_content = "\n\n".join([
        f"Title: {p['title']}\n{p['content']}"
        for p in page_contents
    ])
    
    if not combined_content:
        combined_content = f"Information about {company_name} {role_title} DSA interview questions"
    
    # Step 4: Use LLM to analyze patterns
    print("[DSA] Analyzing patterns with LLM...")
    
    analysis_prompt = f"""
Analyze the following information about {company_name} {role_title} interviews and identify:
1. Most frequently asked DSA topics/problems
2. Common question patterns
3. Difficulty distribution
4. Estimated frequency for each topic

Content:
{combined_content}

Provide analysis in structured format with:
- Question name
- Category
- Frequency score (1-10)
- Difficulty (Easy/Medium/Hard)
- Source count
    """
    
    analysis_schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_name": {"type": "string"},
                        "category": {"type": "string"},
                        "frequency_score": {"type": "integer"},
                        "difficulty": {"type": "string"},
                        "source_count": {"type": "integer"}
                    }
                }
            }
        }
    }
    
    analysis_result = structured_chat(
        analysis_prompt,
        analysis_schema
    )
    
    questions = []
    for item in analysis_result.get("questions", []):
        questions.append(
            RepeatedQuestion(
                question_name=item.get("question_name", ""),
                category=item.get("category", ""),
                frequency_score=item.get("frequency_score", 0),
                difficulty=item.get("difficulty", ""),
                source_count=item.get("source_count", 0)
            )
        )
    
    print(f"[DSA] Analysis complete - Found {len(questions)} key topics")
    
    return questions, source_counts