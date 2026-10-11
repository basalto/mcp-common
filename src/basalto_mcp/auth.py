"""Shared bearer-token auth provider for homelab MCP servers.

``StaticTokenAuth`` verifies a single static bearer token using FastMCP's
auth-provider interface. When ``MCP_AUTH_TOKEN`` is configured, the HTTP
transports (streamable-http / http / sse) require every request to carry a
matching ``Authorization: Bearer <token>`` header; anything else is rejected
with 401.

The token comparison is constant-time (``hmac.compare_digest``) to avoid a
timing side-channel.
"""

from __future__ import annotations

import hmac

from fastmcp.server.auth import AccessToken, TokenVerifier


class StaticTokenAuth(TokenVerifier):
    """Verify a single static bearer token.

    A deliberately minimal provider: no OAuth flow, no refresh, no scopes.
    Exactly one token is accepted. The ``client_id`` only labels the issued
    ``AccessToken``, so it should differ per server.

    Args:
        token: The expected bearer token value. Empty/None means "no token
            configured" — do not construct the provider in that case; the caller
            should skip registering auth instead.
        client_id: Label stamped onto the issued ``AccessToken``.
    """

    def __init__(self, token: str, client_id: str = "basalto-mcp") -> None:
        super().__init__()
        if not token:
            raise ValueError("StaticTokenAuth requires a non-empty token")
        self._token = token
        self._client_id = client_id

    async def verify_token(self, token: str) -> AccessToken | None:
        """Return an ``AccessToken`` when the token matches, else ``None``."""
        if not token:
            return None
        if not hmac.compare_digest(token, self._token):
            return None
        return AccessToken(
            token=token,
            client_id=self._client_id,
            scopes=[],
        )
