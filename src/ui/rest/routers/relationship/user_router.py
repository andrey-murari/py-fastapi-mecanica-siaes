from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.user_dto import UserCreateDTO, UserDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_user import ForManageUser
from src.ui.rest.dependencies import get_for_manage_user, require_admin

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(require_admin)],
)


@user_router.post("/", response_model=UserDTO)
def create_user(
    user: UserCreateDTO,
    use_case: ForManageUser = Depends(get_for_manage_user),
):
    try:
        return use_case.create_user(user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
