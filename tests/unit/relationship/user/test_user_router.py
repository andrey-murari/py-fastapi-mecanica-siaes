from fastapi import HTTPException

from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_manage_relationship.dto.user_dto import UserCreateDTO, UserDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_user import ForManageUser
from src.ui.rest.routers.relationship.user_router import create_user

MECHANIC_CPF = "39053344705"


class _FakeUseCase(ForManageUser):
    def create_user(self, user: UserCreateDTO) -> UserDTO:
        if user.user_type is UserType.ADMIN:
            raise ValueError("User type cannot be registered")
        return UserDTO(
            user_id=user.person_id,
            user_type=user.user_type,
            login=user.person_id,
            password="JM4705",
        )


def test_router_create_delegates_to_port():
    result = create_user(
        UserCreateDTO(
            user_type=UserType.MECHANIC,
            person_id=MECHANIC_CPF,
            complete_name="Jose Mecanico",
        ),
        use_case=_FakeUseCase(),
    )

    assert result.user_id == MECHANIC_CPF
    assert result.login == MECHANIC_CPF
    assert not hasattr(result, "password")


def test_router_create_maps_value_error_to_400():
    try:
        create_user(
            UserCreateDTO(
                user_type=UserType.ADMIN,
                person_id=MECHANIC_CPF,
                complete_name="Admin",
            ),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")
