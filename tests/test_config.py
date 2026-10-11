from pydantic import Field

from basalto_mcp.config import MCPBaseSettings


def test_mcp_auth_token_reads_from_env(monkeypatch):
    monkeypatch.setenv("MCP_AUTH_TOKEN", "tok123")
    s = MCPBaseSettings(_env_file=None)
    assert s.mcp_auth_token == "tok123"


def test_mcp_auth_token_defaults_to_none(monkeypatch):
    monkeypatch.delenv("MCP_AUTH_TOKEN", raising=False)
    s = MCPBaseSettings(_env_file=None)
    assert s.mcp_auth_token is None


def test_subclass_adds_upstream_fields(monkeypatch):
    class ServerSettings(MCPBaseSettings):
        upstream_url: str = Field(default="https://example", validation_alias="UPSTREAM_URL")

    monkeypatch.delenv("MCP_AUTH_TOKEN", raising=False)
    s = ServerSettings(_env_file=None)
    assert s.upstream_url == "https://example"
    assert s.mcp_auth_token is None


def test_subclass_reads_upstream_field_from_env(monkeypatch):
    class ServerSettings(MCPBaseSettings):
        upstream_url: str = Field(default="", validation_alias="UPSTREAM_URL")

    monkeypatch.setenv("UPSTREAM_URL", "https://real.example")
    s = ServerSettings(_env_file=None)
    assert s.upstream_url == "https://real.example"
