from bs4 import BeautifulSoup
import requests

def get_sitemap_urls(website: str):

    sitemap_url = website.rstrip("/") + "/sitemap.xml"

    print(f"\nChecking sitemap:")
    print(sitemap_url)

    try:

        response = requests.get(
            sitemap_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "xml"
        )

        urls = [
            loc.text
            for loc in soup.find_all("loc")
        ]

        print(f"Found {len(urls)} URLs")

        return urls

    except Exception as e:

        print("Failed to load sitemap")
        print(e)

        return []

def filter_urls(urls):

    keywords = [
        "about",
        "company",
        "team",
        "leadership",
        "careers",
        "products",
        "solutions",
        "platform",
        "blog",
        "news",
        "press",
        "Brand",
        "publication",
        "release",
    ]

    selected = []

    for url in urls:

        url_lower = url.lower()

        if any(
            keyword in url_lower
            for keyword in keywords
        ):
            selected.append(url)

    if not selected:
        selected = urls[:10]

    return selected[:15]