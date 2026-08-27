from fastapi import HTTPException

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO, LoginDTO, TokenDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ui.rest.routers.auth.auth_router import login


class _FakeUseCase(ForAuthenticate):
    def login(self, credentials: LoginDTO) -> TokenDTO:
        if credentials.login == "admin" and credentials.password == "secret":
            return TokenDTO(access_token="fake-token")
        raise ValueError("Invalid credentials")

    def current_admin(self, token: str) -> AdminIdentityDTO:
        raise AssertionError("unused")


def test_router_login_delegates_to_port():
    result = login(
        LoginDTO(login="admin", password="secret"),
        use_case=_FakeUseCase(),
    )
    assert result.access_token == "fake-token"
    assert result.token_type == "bearer"


def test_router_login_maps_value_error_to_401():
    try:
        login(
            LoginDTO(login="admin", password="wrong"),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Invalid credentials"
    else:
        raise AssertionError("expected HTTPException")
