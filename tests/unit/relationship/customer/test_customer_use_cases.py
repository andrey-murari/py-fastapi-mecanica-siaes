from datetime import datetime

import pytest

from src.domain.relationship.application.customer_use_cases import CustomerUseCases
from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    AddressInputDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
    PersonAddressCreateDTO,
    PersonDTO,
    VehicleDTO,
)
from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from tests.unit.fakes.in_memory_storage import InMemoryStorage

VALID_CPF = "52998224725"
VALID_CNPJ = "11222333000181"
CEP = "01001000"


def _full_payload(**address_overrides) -> CustomerFullCreateDTO:
    address = {
        "cep_id": CEP,
        "street": "Praça da Sé",
        "neighborhood": "Sé",
        "city": "São Paulo",
        "state": "SP",
        **address_overrides,
    }
    return CustomerFullCreateDTO(
        person_id=VALID_CPF,
        complete_name="Andrey Murari",
        address=AddressInputDTO(**address),
        person_address=PersonAddressCreateDTO(number="100", complement="apto 1"),
    )


class FakeAddresses(ForGetAddress):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def get_address_by_cep(self, cep: str) -> AddressDTO:
        self.calls.append(cep)
        return AddressDTO(
            cep_id=cep,
            street="Praça da Sé",
            neighborhood="Sé",
            city="São Paulo",
            state="SP",
            insertion_date=datetime.now(),
        )


def _seed_vehicle(storage: InMemoryStorage, person_id: str, plate: str = "ABC1D23") -> None:
    storage.save_vehicle(
        VehicleDTO(
            person_id=person_id,
            model="Civic",
            brand="Honda",
            manufacture_year="2020",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
            plate=plate,
            color="Prata",
        )
    )


def test_create_customer_uses_payload_address_when_city_and_state_present():
    storage = InMemoryStorage()
    addresses = FakeAddresses()
    created = CustomerUseCases(storage=storage, address=addresses).create_customer(_full_payload())
    assert created.person_id == VALID_CPF
    assert created.user_id == VALID_CPF
    assert created.flag_customer is True
    assert storage.get_user(VALID_CPF).password == "AM4725"
    assert storage.get_user(VALID_CPF).login == VALID_CPF
    assert addresses.calls == []
    assert storage.addresses[CEP].city == "São Paulo"
    assert storage.people[VALID_CPF].complete_name == "Andrey Murari"
    assert storage.person_addresses[0].number == "100"
    assert storage.person_addresses[0].cep_id == CEP


def test_create_customer_accepts_cnpj():
    storage = InMemoryStorage()
    payload = CustomerFullCreateDTO(
        person_id="11.222.333/0001-81",
        complete_name="Oficina Central",
        address=AddressInputDTO(cep_id=CEP, city="São Paulo", state="SP"),
        person_address=PersonAddressCreateDTO(number="100"),
    )
    created = CustomerUseCases(storage=storage, address=FakeAddresses()).create_customer(payload)
    assert created.person_id == VALID_CNPJ


def test_create_customer_fetches_viacep_when_city_and_state_omitted():
    storage = InMemoryStorage()
    addresses = FakeAddresses()
    payload = CustomerFullCreateDTO(
        person_id=VALID_CPF,
        complete_name="Andrey Murari",
        address=AddressInputDTO(cep_id=CEP),
        person_address=PersonAddressCreateDTO(number="50"),
    )
    created = CustomerUseCases(storage=storage, address=addresses).create_customer(payload)
    assert created.person_id == VALID_CPF
    assert addresses.calls == [CEP]
    assert storage.addresses[CEP].street == "Praça da Sé"


def test_create_customer_reuses_existing_cep():
    storage = InMemoryStorage()
    storage.save_address(
        AddressDTO(
            cep_id=CEP,
            street="Rua Original",
            neighborhood="Centro",
            city="São Paulo",
            state="SP",
        )
    )
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    use_case.create_customer(_full_payload(street="Outra Rua"))
    assert storage.addresses[CEP].street == "Rua Original"


def test_create_customer_rejects_existing_person():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    use_case.create_customer(_full_payload())
    payload = _full_payload()
    with pytest.raises(ValueError, match="Person already exists"):
        use_case.create_customer(payload)


def test_create_customer_rejects_invalid_person_id():
    use_case = CustomerUseCases(storage=InMemoryStorage(), address=FakeAddresses())
    payload = CustomerFullCreateDTO(
        person_id="12345678912",
        complete_name="Andrey Murari",
        address=AddressInputDTO(cep_id=CEP, city="São Paulo", state="SP"),
        person_address=PersonAddressCreateDTO(number="100"),
    )
    with pytest.raises(ValueError, match="Invalid CPF"):
        use_case.create_customer(payload)


def test_read_customer_includes_address():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    detail = use_case.read_customer(created.person_id)
    assert detail.person_id == VALID_CPF
    assert detail.complete_name == "Andrey Murari"
    assert len(detail.addresses) == 1
    assert detail.addresses[0].cep_id == CEP
    assert detail.addresses[0].city == "São Paulo"
    assert detail.addresses[0].person_address is not None
    assert detail.addresses[0].person_address.number == "100"
    assert detail.addresses[0].person_address.complement == "apto 1"
    assert detail.vehicles == []


def test_read_customer_normalizes_formatted_person_id():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    use_case.create_customer(_full_payload())
    assert use_case.read_customer("529.982.247-25").person_id == VALID_CPF


def test_read_customer_requires_customer():
    use_case = CustomerUseCases(storage=InMemoryStorage(), address=FakeAddresses())
    with pytest.raises(ValueError, match="Customer not found"):
        use_case.read_customer(VALID_CPF)


def test_read_customer_ignores_person_without_customer_flag():
    storage = InMemoryStorage()
    storage.save_person(
        PersonDTO(
            person_id=VALID_CPF,
            complete_name="Andrey Murari",
            user_id=VALID_CPF,
            user_modification_id=1,
        )
    )
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    with pytest.raises(ValueError, match="Customer not found"):
        use_case.read_customer(VALID_CPF)


def test_read_customer_rejects_invalid_person_id():
    use_case = CustomerUseCases(storage=InMemoryStorage(), address=FakeAddresses())
    with pytest.raises(ValueError, match="Invalid CPF"):
        use_case.read_customer("12345678912")


def test_read_customer_includes_vehicles():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    _seed_vehicle(storage, created.person_id)
    detail = use_case.read_customer(created.person_id)
    assert len(detail.vehicles) == 1
    assert detail.vehicles[0].model == "Civic"
    assert detail.vehicles[0].plate == "ABC1D23"


def test_update_customer_changes_flag_active():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    updated = use_case.update_customer(created.person_id, CustomerUpdateDTO(flag_active=False))
    assert updated.flag_active is False


def test_delete_customer_removes_person():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    assert use_case.delete_customer(created.person_id) == {"ok": True}
    assert storage.get_person(created.person_id) is None


def test_delete_customer_blocked_when_person_has_vehicles():
    storage = InMemoryStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    _seed_vehicle(storage, created.person_id)
    with pytest.raises(ValueError, match="Person has vehicles"):
        use_case.delete_customer(created.person_id)
