from serpapi import GoogleSearch
from Utils.config import (SERP_API_KEY)


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