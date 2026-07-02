"""
tests/test_analyzer.py — Worker 2
Unit tests for analyzer.py using hardcoded sample data (no live API calls).
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer import (
    calculate_streak,
    longest_streak,
    commits_per_repo,
    commits_per_day,
    most_active_weekday,
    average_pr_merge_time,
)


class FakeCommit:
    def __init__(self, date, repo="test-repo", author="octocat", sha="abc123"):
        self.date = date
        self.repo = repo
        self.author = author
        self.sha = sha


def test_calculate_streak_counts_consecutive_days():
    today = datetime.now()
    commits = [
        FakeCommit(today),
        FakeCommit(today - timedelta(days=1)),
        FakeCommit(today - timedelta(days=2)),
    ]
    assert calculate_streak(commits) == 3


def test_calculate_streak_empty_list_returns_zero():
    """Edge case: no commits should return 0, not crash."""
    assert calculate_streak([]) == 0


def test_calculate_streak_breaks_on_gap():
    today = datetime.now()
    commits = [
        FakeCommit(today),
        FakeCommit(today - timedelta(days=1)),
        FakeCommit(today - timedelta(days=5)),  # gap here
    ]
    assert calculate_streak(commits) == 2


def test_longest_streak_finds_best_run():
    today = datetime.now()
    commits = [
        FakeCommit(today),
        FakeCommit(today - timedelta(days=1)),
        FakeCommit(today - timedelta(days=2)),
        FakeCommit(today - timedelta(days=10)),
        FakeCommit(today - timedelta(days=11)),
    ]
    assert longest_streak(commits) == 3


def test_commits_per_repo_counts_correctly():
    commits = [FakeCommit(datetime.now(), repo="repo-a") for _ in range(3)]
    commits += [FakeCommit(datetime.now(), repo="repo-b")]
    result = commits_per_repo(commits)
    assert result["repo-a"] == 3
    assert result["repo-b"] == 1


def test_commits_per_repo_empty_list_returns_empty_dict():
    """Edge case: empty commit list should return {}, not crash."""
    assert commits_per_repo([]) == {}


def test_commits_per_day_groups_by_date():
    today = datetime.now()
    commits = [
        FakeCommit(today),
        FakeCommit(today),
        FakeCommit(today - timedelta(days=1)),
    ]
    result = commits_per_day(commits)
    assert result[today.date().isoformat()] == 2
    assert result[(today - timedelta(days=1)).date().isoformat()] == 1


def test_most_active_weekday_returns_correct_day():
    monday = datetime(2026, 6, 1)  # a Monday
    tuesday = datetime(2026, 6, 2)
    commits = [FakeCommit(monday), FakeCommit(monday), FakeCommit(tuesday)]
    assert most_active_weekday(commits) == "Monday"


def test_average_pr_merge_time_calculates_correctly():
    pull_requests = [
        {"created_at": "2026-06-01T00:00:00Z", "merged_at": "2026-06-03T00:00:00Z"},  # 2 days
        {"created_at": "2026-06-01T00:00:00Z", "merged_at": "2026-06-05T00:00:00Z"},  # 4 days
    ]
    assert average_pr_merge_time(pull_requests) == 3.0


def test_average_pr_merge_time_skips_unmerged_prs():
    """Edge case: PRs with merged_at=None should be skipped, not crash."""
    pull_requests = [
        {"created_at": "2026-06-01T00:00:00Z", "merged_at": "2026-06-03T00:00:00Z"},  # 2 days
        {"created_at": "2026-06-01T00:00:00Z", "merged_at": None},  # never merged
    ]
    assert average_pr_merge_time(pull_requests) == 2.0


def test_average_pr_merge_time_empty_list_returns_zero():
    """Edge case: empty PR list should return 0.0, not crash."""
    assert average_pr_merge_time([]) == 0.0
    