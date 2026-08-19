from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    url = url.strip().rstrip(".")

    print("Trying URL:", repr(url))

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else "No title"

    for element in soup(["script", "style", "img", "input"]):
        element.decompose()

    text = soup.body.get_text(
        separator="\n",
        strip=True
    ) if soup.body else ""

    return (title + "\n\n" + text)[:2000]


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for tag in soup.find_all("a", href=True):

        link = normalize_url(
            tag["href"],
            url
        )

        # Only keep TTUHSC El Paso links
        if is_same_domain(link):
            links.append(link)

    return list(set(links))

