import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def getPageContent(url_Address):
    session = requests.Session()
    response = session.get(
        url_Address,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
    )
    html_content = response.text

    soup = BeautifulSoup(html_content, "lxml", exclude_encodings="UTF-8")

    for link in soup.find_all("link"):
        href = link.get("href")
        if href:
            if not href.startswith("http"):
                href = urljoin(url_Address, href)
                link["href"] = href
            else:
                link["href"] = href

    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            if not src.startswith("http"):
                src = urljoin(url_Address, src)
                script["src"] = src
            else:
                script["src"] = src

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            if not src.startswith("http"):
                src = urljoin(url_Address, src)
            img["src"] = src

    for a in soup.find_all("link"):
        src = a.get("href")
        if src:
            if not src.startswith("http"):
                src = urljoin(url_Address, src)
            a["src"] = src

    for source in soup.find_all("source"):
        src = source.get("src")
        if src:
            if not src.startswith("http"):
                src = urljoin(url_Address, src)
            source["src"] = src

    return str(soup)
