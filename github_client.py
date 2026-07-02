"""
github_client.py — Worker 1
Thin wrapper around the GitHub REST API for fetching commits, pull requests,
and user activity.
"""

import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from models import Commit

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github+json",
}


def _check_rate_limit(response):
    remaining = response.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) <= 1:
        print(f"[github_client] Warning: only {remaining} API requests remaining.")


def get_user_repos(username: str) -> list[dict]:
    url = f"{BASE_URL}/users/{username}/repos"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        _check_rate_limit(response)

        if response.status_code == 404:
            return []
        if response.status_code == 403:
            print("[github_client] Rate limit exceeded.")
            return []

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("[github_client] Connection error while fetching user repos.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[github_client] Unexpected error fetching user repos: {e}")
        return []


def get_commits(owner: str, repo: str, limit: int = 50) -> list[Commit]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
    params = {"per_page": limit}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        _check_rate_limit(response)

        if response.status_code == 404:
            print(f"[github_client] Repo not found: {owner}/{repo}")
            return []
        if response.status_code == 403:
            print("[github_client] Rate limit exceeded.")
            return []

        response.raise_for_status()
        raw_commits = response.json()

        commits = []
        for item in raw_commits:
            sha = item.get("sha", "")
            commit_data = item.get("commit", {})
            message = commit_data.get("message", "")
            author_info = commit_data.get("author", {})
            author = author_info.get("name", "unknown")
            date_str = author_info.get("date")

            date = None
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    date = None

            commits.append(
                Commit(sha=sha, message=message, author=author, date=date, repo=repo)
            )

        return commits

    except requests.exceptions.ConnectionError:
        print(f"[github_client] Connection error while fetching commits for {owner}/{repo}.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[github_client] Unexpected error fetching commits: {e}")
        return []


def get_pull_requests(owner: str, repo: str) -> list[dict]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "all"}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        _check_rate_limit(response)

        if response.status_code == 404:
            print(f"[github_client] Repo not found: {owner}/{repo}")
            return []
        if response.status_code == 403:
            print("[github_client] Rate limit exceeded.")
            return []

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print(f"[github_client] Connection error while fetching PRs for {owner}/{repo}.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[github_client] Unexpected error fetching pull requests: {e}")
        return []


def get_user_events(username: str) -> list[dict]:
    url = f"{BASE_URL}/users/{username}/events"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        _check_rate_limit(response)

        if response.status_code == 404:
            return []
        if response.status_code == 403:
            print("[github_client] Rate limit exceeded.")
            return []

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("[github_client] Connection error while fetching user events.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[github_client] Unexpected error fetching user events: {e}")
        return []