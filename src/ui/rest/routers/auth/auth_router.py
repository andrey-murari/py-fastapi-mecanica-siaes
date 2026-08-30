from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.ports.driver.for_authenticate.dto import LoginDTO, TokenDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ui.rest.dependencies import get_for_authenticate

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenDTO)
def login(
    credentials: LoginDTO,
    use_case: Annotated[ForAuthenticate, Depends(get_for_authenticate)],
):
    try:
        return use_case.login(credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
