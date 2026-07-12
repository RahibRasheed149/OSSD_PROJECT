# Contributing to OSS Pulse

Thanks for your interest in contributing! This document outlines how our team works on this project, and how any future contributor should get involved.

## Getting started

1. Fork or clone the repository
2. Create a virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
```
3. Create a `.env` file with your own GitHub personal access token:


## Branching strategy

- `main` is protected — all changes must go through a Pull Request
- Create a feature branch off an up-to-date `main`:
```bash
  git checkout main
  git pull origin main
  git checkout -b feature/your-feature-name
```
- Use descriptive branch names, e.g. `feature/dashboard-ui`, `fix/streak-calculation`

## Commit message conventions

We use short prefixes to keep history readable:
- `feat:` — a new feature
- `fix:` — a bug fix
- `docs:` — documentation changes
- `test:` — adding or updating tests
- `refactor:` — code changes that don't add features or fix bugs
- `style:` — formatting, linting fixes

Example:git commit -m "feat: add streak calculation to analyzer"


## Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Run `flake8 .` before pushing to catch style issues early
- Keep functions focused and documented with docstrings

## Pull requests

1. Push your branch and open a PR against `main`
2. Fill in a short description of what changed and why
3. Make sure CI (tests + linter) passes before requesting review
4. At least one other contributor should review before merging

## Reporting bugs or requesting features

Please open a GitHub Issue with:
- A clear, descriptive title
- Steps to reproduce (for bugs) or a description of the desired behavior (for features)
- Any relevant screenshots or error logs

## Running tests locally

```bash
pytest
```

## Questions?

Open an Issue tagged `question`, or reach out to any of the maintainers listed in the README.
