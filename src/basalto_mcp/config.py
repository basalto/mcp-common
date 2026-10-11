"""Shared pydantic-settings base for homelab MCP servers.

Every server's ``Settings`` subclasses :class:`MCPBaseSettings`, which supplies
the ``.env``-loading / case-insensitive / ignore-extra config dict and the one
field identical everywhere — the optional MCP-layer bearer token. All
upstream-specific fields (URLs, credentials, per-service flags) stay on the
server's own subclass with ``validation_alias="UPPER_CASE"``.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPBaseSettings(BaseSettings):
    """Base settings shared by all homelab MCP servers."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    mcp_auth_token: str | None = Field(
        default=None,
        description=(
            "Optional bearer token required on the HTTP transports "
            "(streamable-http / http / sse). When unset, the server runs "
            "unauthenticated."
        ),
        validation_alias="MCP_AUTH_TOKEN",
    )
