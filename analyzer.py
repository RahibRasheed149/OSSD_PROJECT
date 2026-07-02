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

    dates = sorted(set(c.date.date() for c in