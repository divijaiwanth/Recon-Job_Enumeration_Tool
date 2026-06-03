import requests
import trafilatura

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent":
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def scrape_page(
    url: str,
    max_chars: int = 20000
):

    try:

        downloaded = trafilatura.fetch_url(
            url
        )

        if downloaded:

            extracted = (
                trafilatura.extract(
                    downloaded
                )
            )

            if extracted:

                return extracted[
                    :max_chars
                ]

    except Exception:
        pass

    # -------------------
    # Fallback
    # -------------------

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:max_chars]

    except Exception as e:

        print(
            f"[SCRAPER ERROR] {e}"
        )

        return ""