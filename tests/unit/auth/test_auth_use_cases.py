import pytest

from src.domain.relationship.application.auth_use_cases import AuthUseCases
from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_authenticate.dto import LoginDTO, TokenClaimsDTO
from src.ports.driving.for_managing_tokens.for_managing_tokens import ForManagingTokens


class FakeTokens(ForManagingTokens):
    def __init__(self) -> None:
        self.encoded = "fake-token"
        self.claims = TokenClaimsDTO(sub="admin", user_type=UserType.ADMIN.value)

    def encode(self, claims: TokenClaimsDTO) -> str:
        self.claims = claims
        return self.encoded

    def decode(self, token: str) -> TokenClaimsDTO:
        if token != self.encoded:
            raise ValueError("Invalid token")
        return self.claims


def _use_case(tokens: FakeTokens | None = None) -> AuthUseCases:
    return AuthUseCases(
        tokens=tokens or FakeTokens(),
        admin_login="admin",
        admin_password="secret",
    )


def test_login_issues_token_for_admin():
    tokens = FakeTokens()
    result = _use_case(tokens).login(LoginDTO(login="admin", password="secret"))
    assert result.access_token == "fake-token"
    assert result.token_type == "bearer"
    assert tokens.claims.sub == "admin"
    assert tokens.claims.user_type == UserType.ADMIN.value


def test_login_rejects_wrong_password():
    with pytest.raises(ValueError, match="Invalid credentials"):
        _use_case().login(LoginDTO(login="admin", password="wrong"))


def test_login_rejects_wrong_login():
    with pytest.raises(ValueError, match="Invalid credentials"):
        _use_case().login(LoginDTO(login="other", password="secret"))


def test_current_admin_returns_identity():
    identity = _use_case().current_admin("fake-token")
    assert identity.login == "admin"
    assert identity.user_type == UserType.ADMIN.value


def test_current_admin_rejects_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        _use_case().current_admin("not-the-token")


def test_current_admin_rejects_non_admin_type():
    tokens = FakeTokens()
    tokens.claims = TokenClaimsDTO(sub="admin", user_type=UserType.USER.value)
    with pytest.raises(ValueError, match="Invalid token"):
        _use_case(tokens).current_admin("fake-token")
