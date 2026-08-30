import pytest

from src.domain.relationship.application.person_use_cases import PersonUseCases
from src.domain.relationship.application.user_use_cases import UserUseCases
from src.domain.relationship.entities.person import User
from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_manage_relationship.dto.person_dto import PersonCreateDTO
from src.ports.driver.for_manage_relationship.dto.user_dto import UserCreateDTO
from tests.unit.fakes.in_memory_storage import InMemoryStorage

MECHANIC_CPF = "39053344705"
ATTENDANT_CPF = "85351346893"
STOCKIST_CPF = "11144477735"
BUYER_CPF = "71428793860"


def _use_cases() -> tuple[UserUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    return UserUseCases(storage=storage), storage


def _payload(**overrides) -> UserCreateDTO:
    payload = {
        "user_type": UserType.MECHANIC,
        "person_id": MECHANIC_CPF,
        "complete_name": "Jose Mecanico",
    }
    payload.update(overrides)
    return UserCreateDTO(**payload)


def test_credentials_use_cpf_and_initials():
    assert User.credentials_for("52998224725", "Andrey Murari") == ("52998224725", "AM4725")
    assert User.credentials_for("390.533.447-05", "Jose Mecanico") == ("39053344705", "JM4705")


def test_create_staff_users_creates_person_with_cpf_login():
    use_cases, storage = _use_cases()

    created = use_cases.create_user(_payload())
    person = storage.get_person(MECHANIC_CPF)

    assert created.user_id == MECHANIC_CPF
    assert created.login == MECHANIC_CPF
    assert created.password == "JM4705"
    assert created.user_type is UserType.MECHANIC
    assert person is not None
    assert person.user_id == MECHANIC_CPF


def test_create_user_rejects_person_that_already_has_a_user():
    use_cases, storage = _use_cases()
    PersonUseCases(storage).create_person(
        PersonCreateDTO(person_id=MECHANIC_CPF, complete_name="Jose Mecanico")
    )

    payload = _payload()
    with pytest.raises(ValueError, match="Person already has a user"):
        use_cases.create_user(payload)


def test_create_user_rejects_admin():
    use_cases = _use_cases()[0]
    payload = _payload(user_type=UserType.ADMIN)
    with pytest.raises(ValueError, match="User type cannot be registered"):
        use_cases.create_user(payload)


def test_create_other_staff_types():
    use_cases, _ = _use_cases()
    for user_type, person_id, name, password in (
        (UserType.ATTENDANT, ATTENDANT_CPF, "Ana Atendente", "AA6893"),
        (UserType.STOCKIST, STOCKIST_CPF, "Carlos Estoquista", "CE7735"),
        (UserType.BUYER, BUYER_CPF, "Bruno Comprador", "BC3860"),
    ):
        created = use_cases.create_user(
            _payload(user_type=user_type, person_id=person_id, complete_name=name)
        )
        assert created.password == password
        assert created.login == person_id
