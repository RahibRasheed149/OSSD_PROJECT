"""
cache.py — Leader
Simple local caching so repeated dashboard loads for the same username
don't re-hit the GitHub API within a short time window.
"""

import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "data/cache.json"
CACHE_TTL_MINUTES = 15


def get_cached(key: str):
    """Return cached data for a key, or None if missing/expired."""
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        try:
            cache = json.load(f)
        except json.JSONDecodeError:
            return None

    entry = cache.get(key)
    if not entry:
        return None

    cached_time = datetime.fromisoformat(entry["timestamp"])
    if datetime.now() - cached_time > timedelta(minutes=CACHE_TTL_MINUTES):
        return None  # expired

    return entry["data"]


def set_cached(key: str, data):
    """Save data to the cache under the given key, with a timestamp."""
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}

    cache[key] = {
        "timestamp": datetime.now().isoformat(),
        "data": data,
    }

    os.makedirs("data", exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)