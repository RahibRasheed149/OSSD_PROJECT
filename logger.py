import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/errors.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_error(context: str, error: Exception):
    """Call this from any try/except block across the app."""
    logging.error(f"{context}: {str(error)}")