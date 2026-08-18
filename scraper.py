import json
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://ttuhscep.edu/"
DOMAIN = "ttuhscep.edu"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}


def is_same_domain(url):
    """Only allow URLs belonging to ttuhscep.edu."""
    parsed = urlparse(url)

    hostname = parsed.netloc.lower()

    return (
        hostname == DOMAIN
        or hostname.endswith("." + DOMAIN)
    )


def normalize_url(url, base_url):
    """Convert relative URLs into absolute URLs."""
    url = urljoin(base_url, url)

    # Remove #section from URLs
    url = urldefrag(url)[0]

    return url.rstrip("/")


def fetch_page(url):
    """Download a webpage and return its title, text, and links."""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"ERROR: {url}")
        print(e)
        return None

    # Only process HTML pages
    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type:
        print(f"Skipping non-HTML: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Get title
    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "No title"
    )

    # Remove things we don't want in the text
    for element in soup([
        "script",
        "style",
        "noscript",
        "img",
        "input",
        "svg"
    ]):
        element.decompose()

    # Get visible text
    if soup.body:
        text = soup.body.get_text(
            separator="\n",
            strip=True
        )
    else:
        text = ""

    # Find links
    links = []

    for tag in soup.find_all("a", href=True):
        link = normalize_url(
            tag["href"],
            url
        )

        if is_same_domain(link):
            links.append(link)

    return {
        "url": url,
        "title": title,
        "text": text,
        "links": list(set(links))
    }


def crawl_website(start_url, max_pages=100):
    """Crawl ttuhscep.edu starting from start_url."""

    queue = deque([normalize_url(start_url, start_url)])

    visited = set()
    pages = []

    while queue and len(visited) < max_pages:

        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        print(
            f"[{len(visited)}/{max_pages}] "
            f"Crawling: {url}"
        )

        page = fetch_page(url)

        if page is None:
            continue

        pages.append({
            "url": page["url"],
            "title": page["title"],
            "text": page["text"]
        })

        # Add new links to queue
        for link in page["links"]:

            if link not in visited:
                queue.append(link)

        # Be polite to the server
        time.sleep(1)

    return pages


if __name__ == "__main__":

    pages = crawl_website(
        BASE_URL,
        max_pages=100
    )

    with open(
        "ttuhscep_data.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            pages,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print(f"Finished!")
    print(f"Pages collected: {len(pages)}")
    print("Saved to: ttuhscep_data.json")