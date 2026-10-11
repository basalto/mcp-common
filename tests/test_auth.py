import asyncio

import pytest

from basalto_mcp.auth import StaticTokenAuth


def test_constructor_rejects_empty_token():
    with pytest.raises(ValueError):
        StaticTokenAuth("")
    with pytest.raises(ValueError):
        StaticTokenAuth(None)


def test_matching_token_returns_access_token():
    auth = StaticTokenAuth("secret", client_id="test-server")
    token = asyncio.run(auth.verify_token("secret"))
    assert token is not None
    assert token.client_id == "test-server"
    assert token.token == "secret"
    assert token.scopes == []


def test_mismatched_token_returns_none():
    auth = StaticTokenAuth("secret")
    assert asyncio.run(auth.verify_token("wrong")) is None


def test_empty_token_returns_none():
    auth = StaticTokenAuth("secret")
    assert asyncio.run(auth.verify_token("")) is None
    assert asyncio.run(auth.verify_token(None)) is None


def test_default_client_id():
    auth = StaticTokenAuth("secret")
    token = asyncio.run(auth.verify_token("secret"))
    assert token.client_id == "basalto-mcp"
