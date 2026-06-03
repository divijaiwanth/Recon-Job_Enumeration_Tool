from serpapi import GoogleSearch
from Utils.config import SERP_API_KEY
import time
def search_google(
    query: str,
    num_results: int = 10
):

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": num_results
    }

    search = GoogleSearch(
        params
    )

    results = search.get_dict()

    output = []

    for result in results.get(
        "organic_results",
        []
    ):

        output.append(
            {
                "title": result.get(
                    "title",
                    ""
                ),
                "link": result.get(
                    "link",
                    ""
                ),
                "snippet": result.get(
                    "snippet",
                    ""
                )
            }
        )

    return output


def search_interviews(
    company: str,
    role: str
):

    query = (
        f"{company} {role} "
        f"interview experience"
    )

    return search_google(
        query
    )


def search_reddit(
    company: str,
    role: str
):

    query = (
        f"site:reddit.com "
        f"{company} {role} interview"
    )

    return search_google(
        query
    )


def search_glassdoor(
    company: str,
    role: str
):

    query = (
        f"site:glassdoor.com "
        f"{company} {role}"
    )

    return search_google(
        query
    )


def search_dsa(
    company: str
):

    query = (
        f"{company} "
        f"leetcode interview questions"
    )

    return search_google(
        query
    )

def search_with_sources(base_query: str, sources: list[str], max_results_per_source: int = 3):
    """
    Executes multiple Google searches by appending each source to the base query.
    Aggregates the top snippets into a single text block.
    """
    aggregated_snippets = []
    
    for source in sources:
        query = f"{base_query} {source}"
        # Print so user can see it's doing real searches
        print(f"  [Search] {query}")
        try:
            results = search_google(query, num_results=max_results_per_source)
            for res in results:
                snippet = res.get("snippet", "")
                if snippet:
                    aggregated_snippets.append(f"Source ({source}): {snippet}")
            # Small delay to avoid API rate limits if applicable
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Search Error] {e}")
            continue
            
    return "\n".join(aggregated_snippets)