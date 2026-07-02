"""
app.py — Leader
Flask entry point. Wires together data collection (Worker 1),
analysis (Worker 2), and the dashboard UI (Manager).
"""

from flask import Flask, render_template, jsonify

from github_client import get_commits, get_pull_requests, get_user_repos
from logger import log_error
from cache import get_cached, set_cached

app = Flask(__name__)


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
            for repo in repos[:5]:  # limit to first 5 repos to stay within rate limits
                commits = get_commits(username, repo["name"])
                all_commits.extend(commits)

            # TODO: once Worker 2's analyzer.py / charts.py are merged, replace this
            # block with real calculations instead of placeholder values.
            data = {
                "total_commits": len(all_commits),
                "current_streak": 0,
                "avg_pr_merge_time": 0,
                "most_active_repo": repos[0]["name"] if repos else "N/A",
                "line_chart": {"labels": [], "data": []},
                "pie_chart": {"labels": [], "data": []},
                "bar_chart": {"labels": [], "data": []},
                "recent_activity": [],
            }

            set_cached(username, data)

        except Exception as e:
            log_error(f"Building dashboard for {username}", e)
            return render_template("error.html", message="Couldn't load that user's data."), 500

    return render_template("dashboard.html", data=data, username=username)


@app.route("/api/refresh/<username>")
def refresh(username):
    # Force bypass the cache and re-fetch fresh data
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