import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

# Suppress XMLParsedAsHTMLWarning when parsing XML with HTML parser
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def scrape_page(url):

    try:

        print(f"Scraping -> {url}")

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return {
            "url": url,
            "text": text[:15000]
        }

    except Exception as e:

        print(f"Failed -> {url}")

        return {
            "url": url,
            "text": ""
        }


# ==========================================================
# BUILD COMPANY CONTEXT
# ==========================================================

def build_company_context(urls):

    all_text = ""

    for url in urls:

        page = scrape_page(url)

        all_text += "\n\n"
        all_text += f"URL: {page['url']}\n"
        all_text += page["text"]

    return all_text[:50000]