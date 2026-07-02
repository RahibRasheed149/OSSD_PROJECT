"""
scraper.py — Worker 1
Scrapes GitHub's public Trending page (https://github.com/trending) using
BeautifulSoup, since no official API exists for trending repos.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_trending_repos(language: str = None) -> list[dict]:
    """
    Scrape github.com/trending (optionally filtered by language).
    Returns a list of dicts: [{"name": ..., "description": ..., "stars": ...}]
    """
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[scraper] Failed to fetch trending page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    repos = []

    for article in soup.find_all("article", class_="Box-row"):
        try:
            title_tag = article.find("h2")
            if not title_tag or not title_tag.find("a"):
                continue

            name = title_tag.find("a").get_text(strip=True)
            name = " ".join(name.split())
            name = name.replace(" / ", "/")

            desc_tag = article.find("p", class_="col-9")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            star_tag = article.find("a", href=lambda h: h and h.endswith("/stargazers"))
            stars = star_tag.get_text(strip=True) if star_tag else "0"

            repos.append(
                {
                    "name": name,
                    "description": description,
                    "stars": stars,
                }
            )
        except (AttributeError, TypeError) as e:
            print(f"[scraper] Skipping malformed entry: {e}")
            continue

    return repos


if __name__ == "__main__":
    for repo in get_trending_repos()[:10]:
        print(repo)