# OSS Pulse

![CI](https://github.com/RahibRasheed149/OSSD_PROJECT/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

**Developer productivity, indexed.**

OSS Pulse is a Flask web dashboard that turns your GitHub activity into real insight — commit streaks, PR turnaround time, weekday activity patterns, and repo distribution — pulled live from the GitHub REST API and analyzed with pandas.

Built as a semester project for **CS356 — Open Source Software Development** at the University of Management and Technology, Lahore, demonstrating a full open-source development workflow: Git branching, Pull Requests, code review, automated testing, and CI/CD — not just a script that runs once.

---

## Features

- 🔍 **Live GitHub data** — enter any public GitHub username and pull real commit, repo, and pull request activity via the GitHub REST API
- 📊 **Visual analytics** — commit trends over time, repo distribution, and weekday activity, rendered with Chart.js
- 🔥 **Streak tracking** — current and longest consecutive-day commit streaks
- ⏱️ **PR turnaround time** — average time from PR creation to merge
- 📰 **Recent activity feed** — a live log of your most recent commits
- 🌐 **Trending repos** — scrapes GitHub's public Trending page with BeautifulSoup for additional context
- ⚡ **Local caching** — avoids hitting GitHub's API rate limit on repeated dashboard loads
- ✅ **Automated CI/CD** — every push and PR runs linting and tests via GitHub Actions

## Architecture

GitHub REST API + Trending page
│
▼
Data collection (github_client.py, scraper.py, models.py)
│
▼
Analysis (analyzer.py — pandas)
│
▼
Chart formatting (charts.py)
│
▼
Flask app (app.py) + caching (cache.py) + error logging (logger.py)
│
▼
Dashboard UI (templates/, static/) — rendered in the browser


---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Data collection | `requests`, GitHub REST API |
| Web scraping | BeautifulSoup |
| Data analysis | pandas |
| Frontend charts | Chart.js |
| Testing | pytest |
| Linting | flake8 |
| CI/CD | GitHub Actions |

---

## Getting started

### Prerequisites
- Python 3.11+
- A GitHub account (for generating a personal access token)

### Installation

```bash
git clone https://github.com/RahibRasheed149/OSSD_PROJECT.git
cd OSSD_PROJECT
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

GITHUB_TOKEN=your_personal_access_token_here

Generate a token at GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic), with only the `public_repo` scope checked.

### Running locally

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser, enter any public GitHub username, and click **Run**.

### Running tests

```bash
pytest -v
```

### Running the linter

```bash
flake8 .
```

---

## Project structure

OSSD_PROJECT/
├── app.py                    # Flask entry point and routes
├── github_client.py          # GitHub REST API wrapper
├── scraper.py                 # BeautifulSoup Trending page scraper
├── models.py                   # Commit, Contributor, Repository classes
├── analyzer.py                  # Pandas-based data analysis
├── charts.py                     # Chart.js data formatting
├── logger.py                      # Centralized error logging
├── cache.py                        # Local API response caching
├── templates/                       # HTML pages (Jinja2)
├── static/                           # CSS
├── tests/                             # pytest test suite
├── .github/workflows/ci.yml           # GitHub Actions CI pipeline
├── requirements.txt
├── LICENSE
└── CONTRIBUTING.md

---

## Team

Built by a 4-person team for CS356, Spring 2026:

| Role | Responsibilities |
|---|---|
| **Leader** - Rahib Rasheed | Architecture, Flask app, error handling, caching, CI/CD, Git workflow |
| **Designer** - Syeda Samreen Mubasher | Frontend UI, Chart.js integration, documentation |
| **Worker 1** - Ammar Tariq | GitHub API client, web scraping, data models |
| **Worker 2** - Umar Khan | Pandas analysis, chart data formatting |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for our branching strategy, commit conventions, and PR process.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.