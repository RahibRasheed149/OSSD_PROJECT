"""
Demo.py

Demonstrates the four core techniques behind OSS Pulse in a single,
runnable script:

    1. requests       -> pull real commit data from the GitHub REST API
    2. pandas         -> analyze that data (commit streak, most active weekday)
    3. BeautifulSoup  -> scrape GitHub's public Trending page
    4. Flask          -> serve the analyzed data live over HTTP

Run with:
    python Demo.py

The script first prints the requests/pandas/BeautifulSoup results to the
console, then starts a small Flask server so you can see the same data
served live at http://127.0.0.1:5000/api/commits — press Ctrl+C to stop it.

sir this is only the demo version of the OSS Pulse app.py, which is a much larger and more complex application. The real OSS Pulse app.py also includes:

    • a dashboard UI (HTML/CSS/JS) for visualizing the data
    • caching of GitHub API responses to avoid hitting rate limits
    • error handling and logging
    • additional analysis (average PR merge time, commits per repo, etc.)
    • more routes and endpoints for different data views

Optional: set a GITHUB_TOKEN environment variable first to avoid
GitHub's low unauthenticated rate limit (60 requests/hour).
"""

import os
from collections import Counter
from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github+json",
}

DEMO_USERNAME = "octocat"   # a well-known public GitHub account, safe to demo with
DEMO_REPO = "Hello-World"


# ---------------------------------------------------------------------------
# 1. requests — pull real commit data from the GitHub REST API
# ---------------------------------------------------------------------------

def fetch_commits(owner: str, repo: str, limit: int = 20) -> list[dict]:
    """Fetch recent commits for a public repo using the GitHub REST API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": limit}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)

    if response.status_code != 200:
        print(f"[requests] GitHub API returned status {response.status_code}")
        return []

    raw_commits = response.json()
    commits = []
    for item in raw_commits:
        author_info = item.get("commit", {}).get("author", {})
        commits.append({
            "sha": item.get("sha", "")[:7],
            "message": item.get("commit", {}).get("message", "").split("\n")[0],
            "date": author_info.get("date"),
        })

    return commits


# ---------------------------------------------------------------------------
# 2. pandas — analyze the commit data
# ---------------------------------------------------------------------------

def analyze_commits(commits: list[dict]) -> None:
    """Turn raw commit dicts into a DataFrame and print basic insights."""
    if not commits:
        print("[pandas] No commit data to analyze.")
        return

    df = pd.DataFrame(commits)
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.day_name()

    print("\n--- Commit Data (first 5 rows) ---")
    print(df[["sha", "message", "date"]].head())

    weekday_counts = Counter(df["weekday"])
    most_active_day = weekday_counts.most_common(1)[0][0] if weekday_counts else "N/A"

    print(f"\n[pandas] Total commits analyzed: {len(df)}")
    print(f"[pandas] Most active weekday: {most_active_day}")

    # Simple streak calculation, same logic used in OSS Pulse's analyzer.py
    dates = sorted(set(df["date"].dt.date), reverse=True)
    streak = 1 if dates else 0
    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            break

    print(f"[pandas] Current consecutive-day streak (in this sample): {streak}")


# ---------------------------------------------------------------------------
# 3. BeautifulSoup — scrape GitHub's public Trending page
# ---------------------------------------------------------------------------

def fetch_trending_repos(limit: int = 5) -> list[dict]:
    """Scrape github.com/trending for the top trending repos right now."""
    url = "https://github.com/trending"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    if response.status_code != 200:
        print(f"[BeautifulSoup] Failed to fetch trending page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    repos = []

    for article in soup.find_all("article", class_="Box-row")[:limit]:
        title_tag = article.find("h2")
        if not title_tag or not title_tag.find("a"):
            continue

        name = " ".join(title_tag.find("a").get_text(strip=True).split())
        name = name.replace(" / ", "/")

        desc_tag = article.find("p", class_="col-9")
        description = desc_tag.get_text(strip=True) if desc_tag else "(no description)"

        repos.append({"name": name, "description": description})

    return repos


# ---------------------------------------------------------------------------
# 4. Flask — serve the analyzed data as a tiny live web API
# ---------------------------------------------------------------------------
#
# This is the piece that actually ties OSS Pulse together: everything
# above (requests, pandas, BeautifulSoup) produces data — Flask is what
# turns that data into something a browser or another program can
# actually reach over HTTP. This mirrors OSS Pulse's real app.py, just
# reduced to two routes for demonstration purposes.
#
# NOTE: app.run() is a *blocking* call — it starts a live server and
# doesn't return until you stop it. That's why it's kept separate from
# main() below, so the rest of the demo can run and print its output
# first without waiting on a server that never exits on its own.

flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return "OSS Pulse demo API is running. Try /api/commits or /api/trending."


@flask_app.route("/api/commits")
def api_commits():
    """Live endpoint: fetch and return commit data as JSON."""
    commits = fetch_commits(DEMO_USERNAME, DEMO_REPO)
    return jsonify(commits)


@flask_app.route("/api/trending")
def api_trending():
    """Live endpoint: scrape and return trending repos as JSON."""
    trending = fetch_trending_repos()
    return jsonify(trending)


def run_flask_demo():
    """Start the Flask demo server. Blocks until stopped with Ctrl+C."""
    print("\n[4/4] Starting Flask demo server...")
    print("      Visit http://127.0.0.1:5000/api/commits in your browser.")
    print("      Press Ctrl+C to stop.\n")
    flask_app.run(debug=False, port=5000)


# ---------------------------------------------------------------------------
# Main — run all three data demonstrations in sequence
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("OSS PULSE — MINI DEMONSTRATION")
    print("=" * 60)

    print(f"\n[1/3] Fetching commits for {DEMO_USERNAME}/{DEMO_REPO} via requests...")
    commits = fetch_commits(DEMO_USERNAME, DEMO_REPO)

    print(f"\n[2/3] Analyzing {len(commits)} commits with pandas...")
    analyze_commits(commits)

    print("\n[3/3] Scraping GitHub Trending page with BeautifulSoup...")
    trending = fetch_trending_repos()

    print("\n--- Currently Trending on GitHub ---")
    if trending:
        for repo in trending:
            print(f"  • {repo['name']} — {repo['description'][:70]}")
    else:
        print("  (No trending data retrieved — check your connection.)")

    print("\n" + "=" * 60)
    print("Data demonstration complete (requests, pandas, BeautifulSoup).")
    print("Now starting the Flask layer that ties it all together —")
    print("exactly as OSS Pulse's real app.py does.")
    print("=" * 60)

    run_flask_demo()


if __name__ == "__main__":
    main()