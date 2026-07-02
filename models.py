"""
models.py — Worker 1
Defines the core data classes used across the Developer Productivity Dashboard:
Commit, Contributor, and Repository.
"""

from collections import Counter
from datetime import datetime


class Commit:
    def __init__(self, sha, message, author, date, repo):
        self.sha = sha
        self.message = message
        self.author = author
        self.date = date  # stored as a datetime object
        self.repo = repo

    def __repr__(self):
        return f"<Commit {self.sha[:7]} by {self.author} on {self.date}>"


class Contributor:
    def __init__(self, username):
        self.username = username
        self.commits = []  # list of Commit objects

    def add_commit(self, commit):
        """Add a Commit object to this contributor's history."""
        self.commits.append(commit)

    def total_commits(self):
        """Return the total number of commits made by this contributor."""
        return len(self.commits)

    def most_active_day(self):
        """
        Return the weekday (e.g. "Tuesday") on which this contributor
        made the most commits. Returns None if there are no commits.
        """
        if not self.commits:
            return None

        day_counts = Counter(commit.date.strftime("%A") for commit in self.commits)
        return day_counts.most_common(1)[0][0]

    def __repr__(self):
        return f"<Contributor {self.username} ({self.total_commits()} commits)>"


class Repository:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.commits = []
        self.pull_requests = []

    def add_commit(self, commit):
        """Add a Commit object to this repository's history."""
        self.commits.append(commit)

    def add_pull_request(self, pull_request):
        """Add a pull request (dict or object) to this repository."""
        self.pull_requests.append(pull_request)

    def total_commits(self):
        return len(self.commits)

    def total_pull_requests(self):
        return len(self.pull_requests)

    def full_name(self):
        return f"{self.owner}/{self.name}"

    def __repr__(self):
        return f"<Repository {self.full_name()} ({self.total_commits()} commits)>"