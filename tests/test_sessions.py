from backend import sessions
import pytest


def test_create_and_get_session():
    # Skip when Redis is unavailable in local/dev environments.
    try:
        token = sessions.create_session(123)
    except Exception:
        pytest.skip("Redis local não disponível para teste de sessão")
    assert isinstance(token, str) and len(token) > 0
    empresa_id = sessions.get_session_empresa(token)
    assert empresa_id == 123
    sessions.revoke_session(token)
    assert sessions.get_session_empresa(token) is None
