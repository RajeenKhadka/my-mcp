# AGENTS.md

Guidance for AI coding agents working in this repo.

## Project

`my-mcp` is a personal MCP server built with [FastMCP](https://gofastmcp.com), served over HTTP by FastAPI.
Python 3.13, managed with `uv`.

## Layout

```
main.py              FastAPI app: /health route + MCP server mounted at /mcp
app/server.py        Creates the FastMCP instance (`mcp`) and registers every tool
app/db.py            Postgres connection helper (`get_connection()`) for the Neon database
app/tools/           Tool modules, plain Python functions grouped by topic
tests/               pytest tests (create as needed)
start.sh             pip/venv-based setup + run script (no uv required)
requirements.txt     Mirror of pyproject dependencies for start.sh
```

## Commands

```bash
uv sync                                  # install deps (incl. dev group)
uv run uvicorn main:app --reload         # run HTTP server on :8000 (MCP at /mcp, docs at /docs)
uv run fastmcp run app/server.py:mcp     # run MCP server over stdio (e.g. for Claude Code)
uv run pytest                            # run tests
./start.sh                               # alternative: venv + pip + uvicorn (PORT=9000 ./start.sh)
```

## Adding a tool

1. Write a plain, typed function with a docstring in `app/tools/<topic>.py`.
   The type hints and docstring become the tool's schema and description, so keep them accurate.
   ```python
   """<What this group of tools does>."""


   def add(a: int, b: int) -> int:
       """Add two numbers."""
       return a + b
   ```
2. Register it in `app/server.py`:
   ```python
   from app.tools import math_tools

   mcp.add_tool(math_tools.add)
   ```
3. Add a test in `tests/test_<topic>.py` that calls the function directly
   (`from app.tools.<topic> import <fn>`).

Keep tool functions free of FastMCP decorators so they stay easy to unit-test.

## Database

Postgres hosted on [Neon](https://neon.com), accessed with `psycopg` (v3).

- `DATABASE_URL` lives in `.env.local` (git-ignored), written by `neon link`; refresh it with `neon env`.
  `app/db.py` loads that file, but a real `DATABASE_URL` environment variable takes priority.
- Open connections with `with get_connection() as conn:` so they always close.
- Always pass values as query parameters (`conn.execute("... where id = %s", (id,))`), never with f-strings.
- `.neon` (git-ignored) records which Neon project and branch this folder is linked to.

## Conventions

- Import from the `app` package (`from app...`); it is installed as a package and pytest has `pythonpath = ["."]`.
- Each module starts with a short docstring explaining its purpose; comments are brief and explain *why*.
- In `main.py`, the MCP app must be mounted **last** and FastAPI must use `mcp_app.lifespan`, or MCP requests fail.
- When adding a dependency, add it with `uv add <pkg>` **and** add it to `requirements.txt` so `start.sh` keeps working.

## Don'ts

- Never commit `.env` / `.env.*` files or secrets; load config from environment variables.
- Don't commit local data (e.g. `workouts.json`), `.neon`, or `.venv/`.
- Don't edit `uv.lock` by hand.
