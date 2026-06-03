from firecrawl import FirecrawlApp

from Utils.config import (
    FIRECRAWL_API_KEY
)


app = FirecrawlApp(
    api_key=FIRECRAWL_API_KEY
)


def scrape_with_firecrawl(
    url: str
):

    try:

        result = app.scrape_url(
            url=url
        )

        return result

    except Exception as e:

        print(
            f"[FIRECRAWL ERROR] {e}"
        )

        return None