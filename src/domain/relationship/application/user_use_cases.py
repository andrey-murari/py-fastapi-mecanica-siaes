from typing import override

from pydantic import ValidationError

from src.domain.relationship.application.person_login import create_login_for_person
from src.domain.relationship.entities.person import Person
from src.domain.relationship.value_objects.user_type import UserType
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto.person_dto import PersonDTO
from src.ports.driver.for_manage_relationship.dto.user_dto import UserCreateDTO, UserDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_user import ForManageUser
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData

_STAFF = frozenset(
    {
        UserType.MECHANIC,
        UserType.ATTENDANT,
        UserType.STOCKIST,
        UserType.BUYER,
    }
)


class UserUseCases(ForManageUser):
    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_user(self, user: UserCreateDTO) -> UserDTO:
        if user.user_type not in _STAFF:
            raise ValueError("User type cannot be registered")
        try:
            person = Person(
                person_id=user.person_id,
                complete_name=user.complete_name,
                user_modification_id=user.user_modification_id,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        stored = self._storage.get_person(person.person_id)
        if stored is not None and stored.user_id is not None:
            raise ValueError("Person already has a user")

        saved_user = create_login_for_person(
            self._storage,
            person.person_id,
            person.complete_name,
            user.user_type,
            user.user_modification_id,
        )
        self._storage.save_person(
            PersonDTO.model_validate(stored or person).model_copy(
                update={
                    "user_id": saved_user.user_id,
                    "complete_name": person.complete_name,
                    "user_modification_id": user.user_modification_id,
                }
            )
        )
        return saved_user
