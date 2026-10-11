"""Shared building blocks for the basalto homelab MCP servers.

Extracted from the code duplicated across the four FastMCP servers
(netbox / pihole / synology / unifi-mcp-server): the bearer-token auth provider,
the pydantic-settings base, and the standard ``serve()`` entry point.
"""

from .auth import StaticTokenAuth
from .config import MCPBaseSettings
from .server import make_auth, serve

__version__ = "0.1.0"

__all__ = ["StaticTokenAuth", "MCPBaseSettings", "make_auth", "serve", "__version__"]
