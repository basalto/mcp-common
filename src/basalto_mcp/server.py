"""Standard FastMCP server bootstrap shared by homelab MCP servers.

Two helpers:

* :func:`make_auth` builds the ``StaticTokenAuth`` provider (or ``None``) from a
  settings object.
* :func:`serve` is the standard ``main()`` entry point: reads
  ``FASTMCP_TRANSPORT`` / ``FASTMCP_HOST`` / ``FASTMCP_PORT``, serves the HTTP
  transports behind a permissive CORS middleware (M2M tooling calls from
  anywhere on the LAN), and falls back to stdio.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal, cast

from fastmcp import FastMCP

from .auth import StaticTokenAuth

if TYPE_CHECKING:
    from .config import MCPBaseSettings


def make_auth(settings: MCPBaseSettings, *, client_id: str) -> StaticTokenAuth | None:
    """Return a bearer-token provider when a token is configured, else ``None``."""
    if settings.mcp_auth_token:
        return StaticTokenAuth(settings.mcp_auth_token, client_id=client_id)
    return None


def serve(mcp: FastMCP, *, default_port: int) -> None:
    """Run the server: HTTP transport behind CORS, or stdio, per env.

    Args:
        mcp: The configured ``FastMCP`` instance.
        default_port: Port used when ``FASTMCP_PORT`` is unset.
    """
    import uvicorn
    from starlette.middleware.cors import CORSMiddleware

    transport = os.getenv("FASTMCP_TRANSPORT", "stdio")
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", str(default_port)))

    if transport in ("streamable-http", "http", "sse"):
        http_transport = cast(Literal["http", "streamable-http", "sse"], transport)
        starlette_app = mcp.http_app(transport=http_transport)
        cors_app = CORSMiddleware(
            app=starlette_app,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        uvicorn.run(cors_app, host=host, port=port, lifespan="on")
    else:
        run_transport = cast(Literal["stdio", "http", "sse", "streamable-http"], transport)
        mcp.run(transport=run_transport)
