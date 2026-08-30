from src.domain.relationship.entities.person import User
from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_manage_relationship.dto.user_dto import UserDTO
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


def create_login_for_person(
    storage: ForStoringData,
    person_id: str,
    complete_name: str,
    user_type: UserType,
    user_modification_id: int = 1,
) -> UserDTO:
    login, password = User.credentials_for(person_id, complete_name)
    if storage.get_user(login) is not None or storage.get_user_by_login(login) is not None:
        raise ValueError("Login already exists")
    return storage.save_user(
        UserDTO(
            user_id=login,
            user_type=user_type,
            login=login,
            password=password,
            user_modification_id=user_modification_id,
        )
    )
