from datetime import datetime, timedelta, timezone
from typing import override

import jwt

from src.ports.driver.for_authenticate.dto import TokenClaimsDTO
from src.ports.driving.for_managing_tokens.for_managing_tokens import ForManagingTokens

_ALGORITHM = "HS256"


class PyJwtAdapter(ForManagingTokens):
    def __init__(self, secret: str, expire_minutes: int = 60) -> None:
        if not secret:
            raise ValueError("JWT secret is required")
        self._secret = secret
        self._expire_minutes = expire_minutes

    @override
    def encode(self, claims: TokenClaimsDTO) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": claims.sub,
            "user_type": claims.user_type,
            "iat": now,
            "exp": now + timedelta(minutes=self._expire_minutes),
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    @override
    def decode(self, token: str) -> TokenClaimsDTO:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[_ALGORITHM])
        except jwt.PyJWTError as exc:
            raise ValueError("Invalid token") from exc
        sub = payload.get("sub")
        user_type = payload.get("user_type")
        if not sub or not user_type:
            raise ValueError("Invalid token")
        return TokenClaimsDTO(sub=sub, user_type=user_type)
