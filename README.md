"""Shared building blocks for homelab MCP servers.

This package is the single source of truth for the code that was copy-pasted
across the four basalto FastMCP servers (netbox, pihole, synology, unifi):

* ``basalto_mcp.auth.StaticTokenAuth`` — bearer-token verifier (401 on mismatch).
* ``basalto_mcp.config.MCPBaseSettings`` — pydantic-settings base + ``MCP_AUTH_TOKEN``.
* ``basalto_mcp.server.make_auth`` / ``serve`` — auth wiring + standard entry point.

## Consuming it

Add it as a git dependency pinned to a release tag, then subclass the base and
reuse the helpers:

```toml
dependencies = [
    "basalto-mcp @ git+https://github.com/basalto/mcp-common@v0.1.0",
]
```

```python
from basalto_mcp import MCPBaseSettings, make_auth, serve
from fastmcp import FastMCP

class Settings(MCPBaseSettings):
    upstream_url: str = Field(..., validation_alias="UPSTREAM_URL")
    # ... upstream-specific fields ...

settings = Settings()
mcp = FastMCP("My MCP Server", auth=make_auth(settings, client_id="my-mcp-server"))

@mcp.tool()
async def health_check() -> dict:
    return {"status": "healthy"}

def main() -> None:
    serve(mcp, default_port=3100)
```

The upstream client (``client.py``) is intentionally NOT shared — it encodes the
auth/error/re-auth quirks of a specific upstream API and belongs in each repo.
