import pytest

from src.domain.relationship.application.auth_use_cases import AuthUseCases
from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_authenticate.dto import LoginDTO, TokenClaimsDTO
from src.ports.driver.for_manage_relationship.dto.user_dto import UserDTO
from src.ports.driving.for_managing_tokens.for_managing_tokens import ForManagingTokens
from tests.unit.fakes.in_memory_storage import InMemoryStorage

MECHANIC_LOGIN = "39053344705"
MECHANIC_PASSWORD = "JM4705"


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


def _storage_with_mechanic(*, flag_active: bool = True) -> InMemoryStorage:
    storage = InMemoryStorage()
    storage.save_user(
        UserDTO(
            user_id=MECHANIC_LOGIN,
            user_type=UserType.MECHANIC,
            login=MECHANIC_LOGIN,
            password=MECHANIC_PASSWORD,
            flag_active=flag_active,
        )
    )
    return storage


def _use_case(
    tokens: FakeTokens | None = None,
    storage: InMemoryStorage | None = None,
) -> AuthUseCases:
    return AuthUseCases(
        tokens=tokens or FakeTokens(),
        admin_login="admin",
        admin_password="secret",
        storage=storage or InMemoryStorage(),
    )


def test_login_issues_token_for_admin():
    tokens = FakeTokens()
    result = _use_case(tokens).login(LoginDTO(login="admin", password="secret"))
    assert result.access_token == "fake-token"
    assert result.token_type == "bearer"
    assert tokens.claims.sub == "admin"
    assert tokens.claims.user_type == UserType.ADMIN.value


def test_login_rejects_wrong_password():
    use_case = _use_case()
    payload = LoginDTO(login="admin", password="wrong")
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.login(payload)


def test_login_rejects_wrong_login():
    use_case = _use_case()
    payload = LoginDTO(login="other", password="secret")
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.login(payload)


def test_current_admin_returns_identity():
    identity = _use_case().current_admin("fake-token")
    assert identity.login == "admin"
    assert identity.user_type == UserType.ADMIN.value


def test_current_admin_rejects_invalid_token():
    use_case = _use_case()
    with pytest.raises(ValueError, match="Invalid token"):
        use_case.current_admin("not-the-token")


def test_current_admin_rejects_non_admin_type():
    tokens = FakeTokens()
    tokens.claims = TokenClaimsDTO(sub="admin", user_type=UserType.USER.value)
    use_case = _use_case(tokens)
    with pytest.raises(ValueError, match="Invalid token"):
        use_case.current_admin("fake-token")


def test_login_issues_token_for_registered_user_with_role():
    tokens = FakeTokens()
    result = _use_case(tokens, _storage_with_mechanic()).login(
        LoginDTO(login=MECHANIC_LOGIN, password=MECHANIC_PASSWORD)
    )
    assert result.access_token == "fake-token"
    assert tokens.claims.sub == MECHANIC_LOGIN
    assert tokens.claims.user_type == UserType.MECHANIC.value


def test_login_rejects_registered_user_wrong_password():
    use_case = _use_case(storage=_storage_with_mechanic())
    payload = LoginDTO(login=MECHANIC_LOGIN, password="wrong")
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.login(payload)


def test_login_rejects_inactive_user():
    use_case = _use_case(storage=_storage_with_mechanic(flag_active=False))
    payload = LoginDTO(login=MECHANIC_LOGIN, password=MECHANIC_PASSWORD)
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.login(payload)
