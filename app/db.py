"""Postgres connection helper for the Neon database.

The connection string comes from DATABASE_URL, which `neon link` writes to .env.local.
"""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Load .env.local from the project root, wherever the server is started from.
# Real environment variables win, so production can set DATABASE_URL directly.
load_dotenv(Path(__file__).resolve().parent.parent / ".env.local")


def get_connection() -> psycopg.Connection:
    """Open a new connection to the database. Use it in a `with` block so it closes."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Run `neon link` or add it to .env.local.")
    return psycopg.connect(url)
