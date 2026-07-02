"""
charts.py — Worker 2
Reformats analyzer.py output into JSON-serializable dicts shaped for
Chart.js on the frontend. No new analysis logic lives here — these
functions only call analyzer.py and reshape the results.
"""

from analyzer import commits_per_day, commits_per_repo, commits_to_dataframe

WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def prepare_line_chart_data(commits: list) -> dict:
    """
    Returns data shaped for a Chart.js line chart of commits over time.
    Format:
    {
        "labels": ["2026-06-01", "2026-06-02", ...],
        "data": [4, 7, 2, ...]
    }
    """
    daily_counts = commits_per_day(commits)

    return {
        "labels": list(daily_counts.keys()),
        "data": list(daily_counts.values()),
    }


def prepare_repo_distribution_data(commits: list) -> dict:
    """
    Returns data shaped for a Chart.js doughnut/pie chart.
    Format:
    {
        "labels": ["oss-pulse", "roshni-finance", ...],
        "data": [52, 31, 17]
    }
    """
    repo_counts = commits_per_repo(commits)

    return {
        "labels": list(repo_counts.keys()),
        "data": list(repo_counts.values()),
    }


def prepare_weekday_bar_data(commits: list) -> dict:
    """
    Returns data shaped for a Chart.js bar chart, Monday through Sunday.
    Format:
    {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [3, 6, 4, 8, 5, 2, 7]
    }
    """
    if not commits:
        return {"labels": WEEKDAY_LABELS, "data": [0] * 7}

    df = commits_to_dataframe(commits)
    if df.empty:
        return {"labels": WEEKDAY_LABELS, "data": [0] * 7}

    weekday_counts = df["weekday"].value_counts().to_dict()
    data = [weekday_counts.get(day, 0) for day in WEEKDAY_ORDER]

    return {
        "labels": WEEKDAY_LABELS,
        "data": data,
    }