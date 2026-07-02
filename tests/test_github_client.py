"""
tests/test_github_client.py — Worker 1
Unit tests for github_client.py using mock data (no live API calls).
"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from github_client import get_commits, get_pull_requests, get_user_repos


@patch("github_client.requests.get")
def test_get_commits_returns_list(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"X-RateLimit-Remaining": "59"}
    mock_response.json.return_value = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Fix bug",
                "author": {"name": "octocat", "date": "2026-06-01T10:00:00Z"},
            },
        }
    ]
    mock_get.return_value = mock_response

    result = get_commits("octocat", "Hello-World")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].sha == "abc123"
    assert result[0].message == "Fix bug"
    assert result[0].author == "octocat"


@patch("github_client.requests.get")
def test_get_commits_invalid_repo_returns_empty_list(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.headers = {}
    mock_get.return_value = mock_response

    result = get_commits("nonexistent-user", "nonexistent-repo")

    assert result == []


@patch("github_client.requests.get")
def test_get_commits_rate_limited_returns_empty_list(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.headers = {"X-RateLimit-Remaining": "0"}
    mock_get.return_value = mock_response

    result = get_commits("octocat", "Hello-World")

    assert result == []


@patch("github_client.requests.get")
def test_get_pull_requests_returns_list(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"X-RateLimit-Remaining": "58"}
    mock_response.json.return_value = [
        {"number": 1, "title": "Add feature", "state": "open"},
        {"number": 2, "title": "Fix typo", "state": "closed"},
    ]
    mock_get.return_value = mock_response

    result = get_pull_requests("octocat", "Hello-World")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "Add feature"


@patch("github_client.requests.get")
def test_get_user_repos_returns_list(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"X-RateLimit-Remaining": "57"}
    mock_response.json.return_value = [
        {"name": "Hello-World", "full_name": "octocat/Hello-World"}
    ]
    mock_get.return_value = mock_response

    result = get_user_repos("octocat")

    assert isinstance(result, list)
    assert result[0]["name"] == "Hello-World"


@patch("github_client.requests.get")
def test_get_user_repos_connection_error_returns_empty_list(mock_get):
    import requests

    mock_get.side_effect = requests.exceptions.ConnectionError()

    result = get_user_repos("octocat")

    assert result == []