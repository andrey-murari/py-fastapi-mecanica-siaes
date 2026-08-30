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
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


def _same_secret(left: str, right: str) -> bool:
    return len(left) == len(right) and secrets.compare_digest(left, right)


class AuthUseCases(ForAuthenticate):
    """Implements the driver port and depends only on driven ports."""

    def __init__(
        self,
        tokens: ForManagingTokens,
        admin_login: str,
        admin_password: str,
        storage: ForStoringData,
    ) -> None:
        self._tokens = tokens
        self._admin_login = admin_login
        self._admin_password = admin_password
        self._storage = storage

    @override
    def login(self, credentials: LoginDTO) -> TokenDTO:
        if _same_secret(credentials.login, self._admin_login):
            if not _same_secret(credentials.password, self._admin_password):
                raise ValueError("Invalid credentials")
            return TokenDTO(
                access_token=self._tokens.encode(
                    TokenClaimsDTO(sub=credentials.login, user_type=UserType.ADMIN.value)
                )
            )
        user = self._storage.get_user_by_login(credentials.login)
        if (
            user is None
            or not user.flag_active
            or not _same_secret(credentials.password, user.password)
        ):
            raise ValueError("Invalid credentials")
        return TokenDTO(
            access_token=self._tokens.encode(
                TokenClaimsDTO(sub=user.login, user_type=user.user_type.value)
            )
        )

    @override
    def current_admin(self, token: str) -> AdminIdentityDTO:
        claims = self._tokens.decode(token)
        if claims.user_type != UserType.ADMIN.value:
            raise ValueError("Invalid token")
        return AdminIdentityDTO(login=claims.sub, user_type=claims.user_type)
