"""The MCP server: creates the FastMCP instance and registers every tool.

Run it on its own over stdio (for Claude Code):
    uv run fastmcp run app/server.py:mcp
"""

from fastmcp import FastMCP

from app.tools import math_tools

mcp = FastMCP("my-mcp")

mcp.add_tool(math_tools.add)
