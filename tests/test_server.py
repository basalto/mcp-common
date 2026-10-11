from basalto_mcp.server import make_auth, serve


class FakeSettings:
    def __init__(self, token):
        self.mcp_auth_token = token


def test_make_auth_returns_provider_when_token_set():
    auth = make_auth(FakeSettings("tok"), client_id="test")
    assert auth is not None
    assert auth._client_id == "test"


def test_make_auth_returns_none_without_token():
    assert make_auth(FakeSettings(None), client_id="test") is None
    assert make_auth(FakeSettings(""), client_id="test") is None


def test_serve_stdio_calls_mcp_run(monkeypatch):
    calls = {}

    class FakeMCP:
        def run(self, transport):
            calls["run"] = transport

        def http_app(self, transport):
            calls["http_app"] = transport

    monkeypatch.setenv("FASTMCP_TRANSPORT", "stdio")
    monkeypatch.delenv("FASTMCP_PORT", raising=False)
    serve(FakeMCP(), default_port=3001)
    assert calls == {"run": "stdio"}


def test_serve_http_builds_cors_app(monkeypatch):
    import uvicorn
    from starlette.middleware.cors import CORSMiddleware

    calls = {}

    class FakeMCP:
        def run(self, transport):
            calls["run"] = transport

        def http_app(self, transport):
            calls["http_app"] = transport
            return "STARLETTE_APP"

    monkeypatch.setenv("FASTMCP_TRANSPORT", "streamable-http")
    monkeypatch.setenv("FASTMCP_PORT", "9999")

    monkeypatch.setattr(
        uvicorn,
        "run",
        lambda app, host, port, lifespan: calls.update(
            app=app, host=host, port=port, lifespan=lifespan
        ),
    )
    original_init = CORSMiddleware.__init__

    def capture_init(self, app, **kwargs):
        calls["cors_app"] = app
        original_init(self, app=app, **kwargs)

    monkeypatch.setattr(CORSMiddleware, "__init__", capture_init)

    serve(FakeMCP(), default_port=3001)

    assert calls["http_app"] == "streamable-http"
    assert calls["cors_app"] == "STARLETTE_APP"
    assert calls["host"] == "0.0.0.0"
    assert calls["port"] == 9999
    assert calls["lifespan"] == "on"
