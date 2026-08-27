import secrets
from typing import override

from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_authenticate.dto import (
    AdminIdentityDTO,
    LoginDTO,
    TokenClaimsDTO,
    TokenDTO,
)
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driving.for_managing_tokens.for_managing_tokens import ForManagingTokens


class AuthUseCases(ForAuthenticate):
    """Implements the driver port and depends only on driven ports."""

    def __init__(
        self,
        tokens: ForManagingTokens,
        admin_login: str,
        admin_password: str,
    ) -> None:
        self._tokens = tokens
        self._admin_login = admin_login
        self._admin_password = admin_password

    @override
    def login(self, credentials: LoginDTO) -> TokenDTO:
        login_ok = secrets.compare_digest(credentials.login, self._admin_login)
        password_ok = secrets.compare_digest(credentials.password, self._admin_password)
        if not (login_ok and password_ok):
            raise ValueError("Invalid credentials")
        token = self._tokens.encode(
            TokenClaimsDTO(sub=credentials.login, user_type=UserType.ADMIN.value)
        )
        return TokenDTO(access_token=token)

    @override
    def current_admin(self, token: str) -> AdminIdentityDTO:
        claims = self._tokens.decode(token)
        if claims.user_type != UserType.ADMIN.value:
            raise ValueError("Invalid token")
        return AdminIdentityDTO(login=claims.sub, user_type=claims.user_type)
