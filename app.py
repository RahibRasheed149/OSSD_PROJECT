"""
app.py — Leader
Flask entry point. Wires together data collection (Worker 1),
analysis (Worker 2), and the dashboard UI (Manager).
"""

from datetime import datetime

from flask import Flask, render_template, jsonify

from github_client import get_commits, get_pull_requests, get_user_repos
from analyzer import (
    calculate_streak,
    commits_per_repo,
    average_pr_merge_time,
)
from charts import (
    prepare_line_chart_data,
    prepare_repo_distribution_data,
    prepare_weekday_bar_data,
)
from logger import log_error
from cache import get_cached, set_cached

app = Flask(__name__)


def build_recent_activity(commits, limit=5):
    """Build a simple recent-activity list from the most recent commits."""
    sorted_commits = sorted(
        [c for c in commits if c.date is not None],
        key=lambda c: c.date,
        reverse=True
    )

    activity = []
    for c in sorted_commits[:limit]:
        days_ago = (datetime.now() - c.date).days
        if days_ago == 0:
            time_ago = "today"
        elif days_ago == 1:
            time_ago = "1 day ago"
        else:
            time_ago = f"{days_ago} days ago"

        activity.append({
            "message": c.message.split("\n")[0][:60],  # first line, trimmed
            "repo": c.repo,
            "time_ago": time_ago,
        })

    return activity


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard/<username>")
def dashboard(username):
    cached = get_cached(username)
    if cached:
        data = cached
    else:
        try:
            repos = get_user_repos(username)

            all_commits = []
            all_prs = []
            for repo in repos[:5]:  # limit to first 5 repos to respect rate limits
                commits = get_commits(username, repo["name"])
                all_commits.extend(commits)
                prs = get_pull_requests(username, repo["name"])
                all_prs.extend(prs)

            repo_counts = commits_per_repo(all_commits)
            most_active = max(repo_counts, key=repo_counts.get) if repo_counts else "N/A"

            data = {
                "total_commits": len(all_commits),
                "current_streak": calculate_streak(all_commits),
                "avg_pr_merge_time": average_pr_merge_time(all_prs),
                "most_active_repo": most_active,
                "line_chart": prepare_line_chart_data(all_commits),
                "pie_chart": prepare_repo_distribution_data(all_commits),
                "bar_chart": prepare_weekday_bar_data(all_commits),
                "recent_activity": build_recent_activity(all_commits),
            }

            set_cached(username, data)

        except Exception as e:
            log_error(f"Building dashboard for {username}", e)
            return render_template("error.html", message="Couldn't load that user's data."), 500

    return render_template("dashboard.html", data=data, username=username)


@app.route("/api/refresh/<username>")
def refresh(username):
    try:
        repos = get_user_repos(username)
        all_commits = []
        for repo in repos[:5]:
            commits = get_commits(username, repo["name"])
            all_commits.extend(commits)

        data = {"total_commits": len(all_commits)}
        set_cached(username, data)
        return jsonify(data)

    except Exception as e:
        log_error(f"Refreshing dashboard for {username}", e)
        return jsonify({"error": "Failed to refresh data"}), 500


if __name__ == "__main__":
    app.run(debug=True)