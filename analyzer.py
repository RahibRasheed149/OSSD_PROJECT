"""
analyzer.py — Worker 2
Pandas logic for turning raw Commit/PR data (from Worker 1) into stats:
streaks, commit frequency, PR turnaround time.
"""

import pandas as pd
from datetime import datetime, timedelta
from collections import Counter


def commits_to_dataframe(commits: list) -> pd.DataFrame:
    """Convert a list of Commit objects into a pandas DataFrame."""
    data = [
        {
            "sha": c.sha,
            "author": c.author,
            "date": c.date,
            "repo": c.repo,
            "weekday": c.date.strftime("%A"),
        }
        for c in commits
        if c.date is not None
    ]
    return pd.DataFrame(data)


def calculate_streak(commits: list) -> int:
    """
    Return the current consecutive-day commit streak.
    Counts backward from the most recent commit date while each day
    has at least one commit. Returns 0 if there are no commits.
    """
    if not commits:
        return 0

    dates = sorted(set(c.date.date() for c in commits if c.date is not None), reverse=True)
    if not dates:
        return 0

    streak = 1
    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            break

    return streak


def longest_streak(commits: list) -> int:
    """Return the longest streak of consecutive days with at least one commit, ever."""
    if not commits:
        return 0

    dates = sorted(set(c.date.date() for c in commits if c.date is not None))
    if not dates:
        return 0

    longest = 1
    current = 1
    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def commits_per_day(commits: list) -> dict:
    """Return {date_string: commit_count} for charting a line/bar graph."""
    if not commits:
        return {}

    counter = Counter(
        c.date.date().isoformat() for c in commits if c.date is not None
    )
    return dict(sorted(counter.items()))


def most_active_weekday(commits: list) -> str:
    """Return the weekday with the highest total commit count across all data."""
    if not commits:
        return "N/A"

    counter = Counter(
        c.date.strftime("%A") for c in commits if c.date is not None
    )
    if not counter:
        return "N/A"

    return counter.most_common(1)[0][0]


def commits_per_repo(commits: list) -> dict:
    """Return {repo_name: commit_count} — used for the repo distribution chart."""
    if not commits:
        return {}

    counter = Counter(c.repo for c in commits)
    return dict(counter)


def average_pr_merge_time(pull_requests: list) -> float:
    """
    Given a list of PR dicts with 'created_at' and 'merged_at' fields,
    return the average time-to-merge in days. Skips PRs that were never merged.
    """
    if not pull_requests:
        return 0.0

    merge_times = []
    for pr in pull_requests:
        created_str = pr.get("created_at")
        merged_str = pr.get("merged_at")

        if not created_str or not merged_str:
            continue

        try:
            created = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%SZ")
            merged = datetime.strptime(merged_str, "%Y-%m-%dT%H:%M:%SZ")
            delta_days = (merged - created).total_seconds() / 86400
            merge_times.append(delta_days)
        except (ValueError, TypeError):
            continue

    if not merge_times:
        return 0.0

    return round(sum(merge_times) / len(merge_times), 2)