from datetime import datetime, timedelta, timezone

import jwt
import pytest

from src.adapters.driving.for_managing_tokens.pyjwt_adapter import PyJwtAdapter
from src.ports.driver.for_authenticate.dto import TokenClaimsDTO

SECRET = "test-secret"
CLAIMS = TokenClaimsDTO(sub="admin", user_type="Administrador")


def test_encode_decode_roundtrip():
    adapter = PyJwtAdapter(secret=SECRET, expire_minutes=60)
    token = adapter.encode(CLAIMS)
    decoded = adapter.decode(token)
    assert decoded.sub == "admin"
    assert decoded.user_type == "Administrador"


def test_decode_rejects_expired_token():
    adapter = PyJwtAdapter(secret=SECRET, expire_minutes=-1)
    token = adapter.encode(CLAIMS)
    with pytest.raises(ValueError, match="Invalid token"):
        adapter.decode(token)


def test_decode_rejects_wrong_secret():
    token = PyJwtAdapter(secret=SECRET).encode(CLAIMS)
    other = PyJwtAdapter(secret="other-secret")
    with pytest.raises(ValueError, match="Invalid token"):
        other.decode(token)


def test_decode_rejects_tampered_token():
    adapter = PyJwtAdapter(secret=SECRET)
    token = adapter.encode(CLAIMS)
    tampered = token[:-4] + ("A" if token[-4] != "A" else "B") + token[-3:]
    with pytest.raises(ValueError, match="Invalid token"):
        adapter.decode(tampered)


def test_decode_rejects_missing_claims():
    adapter = PyJwtAdapter(secret=SECRET)
    token = jwt.encode(
        {
            "sub": "admin",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
        },
        SECRET,
        algorithm="HS256",
    )
    with pytest.raises(ValueError, match="Invalid token"):
        adapter.decode(token)


def test_adapter_requires_secret():
    with pytest.raises(ValueError, match="JWT secret is required"):
        PyJwtAdapter(secret="")
