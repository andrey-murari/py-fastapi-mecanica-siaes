from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO, LoginDTO, TokenDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ui.rest.dependencies import require_admin


class _FakeAuth(ForAuthenticate):
    def login(self, credentials: LoginDTO) -> TokenDTO:
        raise AssertionError("unused")

    def current_admin(self, token: str) -> AdminIdentityDTO:
        if token == "valid-token":
            return AdminIdentityDTO(login="admin", user_type="Administrador")
        raise ValueError("Invalid token")


def test_require_admin_missing_credentials():
    try:
        require_admin(credentials=None, auth=_FakeAuth())
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Not authenticated"
    else:
        raise AssertionError("expected HTTPException")


def test_require_admin_invalid_token():
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad")
    try:
        require_admin(credentials=credentials, auth=_FakeAuth())
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Invalid token"
    else:
        raise AssertionError("expected HTTPException")


def test_require_admin_valid_token():
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid-token")
    identity = require_admin(credentials=credentials, auth=_FakeAuth())
    assert identity.login == "admin"
    assert identity.user_type == "Administrador"
