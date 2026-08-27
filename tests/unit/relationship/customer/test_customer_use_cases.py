from datetime import datetime

import pytest
from pydantic import ValidationError

from src.domain.relationship.application.customer_use_cases import CustomerUseCases
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    AddressInputDTO,
    CustomerCreateDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    PersonAddressCreateDTO,
    PersonAddressDTO,
    PersonDTO,
)
from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData

VALID_CPF = "52998224725"
CEP = "01001000"


def _person_dto(cpf: str = VALID_CPF) -> PersonDTO:
    return PersonDTO(
        cpf=cpf,
        complete_name="Andrey Murari",
        user_id=1,
        user_modification_id=1,
    )


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
        cpf=VALID_CPF,
        complete_name="Andrey Murari",
        address=AddressInputDTO(**address),
        person_address=PersonAddressCreateDTO(number="100", complement="apto 1"),
    )


class FakeStorage(ForStoringData):
    def __init__(self) -> None:
        self.customers: dict[int, CustomerDTO] = {}
        self.customers_by_cpf: dict[str, CustomerDTO] = {}
        self.people: dict[str, PersonDTO] = {}
        self.addresses: dict[str, AddressDTO] = {}
        self.person_addresses: list[PersonAddressDTO] = []
        self._next_customer_id = 1
        self._next_person_address_id = 1

    def create_db_and_tables(self) -> None:
        return None

    def close(self) -> None:
        return None

    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        return self.customers.get(customer_id)

    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        return self.customers_by_cpf.get(cpf)

    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        dto = CustomerDTO.model_validate(customer)
        if dto.customer_id is None:
            dto = dto.model_copy(update={"customer_id": self._next_customer_id})
            self._next_customer_id += 1
        self.customers[dto.customer_id] = dto
        self.customers_by_cpf[dto.cpf] = dto
        return dto

    def delete_customer(self, customer_id: int) -> None:
        row = self.customers.pop(customer_id, None)
        if row is not None:
            self.customers_by_cpf.pop(row.cpf, None)

    def get_person(self, cpf: str) -> PersonDTO | None:
        return self.people.get(cpf)

    def save_person(self, person: PersonDTO) -> PersonDTO:
        dto = PersonDTO.model_validate(person)
        self.people[dto.cpf] = dto
        return dto

    def get_address(self, cep_id: str) -> AddressDTO | None:
        return self.addresses.get(cep_id)

    def get_person_addresses(self, cpf: str) -> list[PersonAddressDTO]:
        return [row for row in self.person_addresses if row.cpf == cpf]

    def save_address(self, address: AddressDTO) -> AddressDTO:
        dto = AddressDTO.model_validate(address)
        self.addresses[dto.cep_id] = dto
        return dto

    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        dto = PersonAddressDTO.model_validate(person_address)
        if dto.person_address_id is None:
            dto = dto.model_copy(update={"person_address_id": self._next_person_address_id})
            self._next_person_address_id += 1
        self.person_addresses.append(dto)
        return dto

    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        if address.cep_id not in self.addresses:
            self.save_address(address)
        self.save_person(person)
        self.save_person_address(person_address)
        return self.save_customer(customer)


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


def test_create_customer_only_cpf_requires_existing_person():
    use_case = CustomerUseCases(storage=FakeStorage(), address=FakeAddresses())
    with pytest.raises(ValueError, match="Person not found"):
        use_case.create_customer_only_cpf(CustomerCreateDTO(cpf=VALID_CPF))


def test_create_customer_only_cpf_saves_when_person_exists():
    storage = FakeStorage()
    storage.save_person(_person_dto())
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer_only_cpf(CustomerCreateDTO(cpf=VALID_CPF))
    assert created.customer_id == 1
    assert created.cpf == VALID_CPF
    assert storage.get_customer_by_cpf(VALID_CPF) is not None


def test_create_customer_only_cpf_rejects_duplicate_customer():
    storage = FakeStorage()
    storage.save_person(_person_dto())
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    use_case.create_customer_only_cpf(CustomerCreateDTO(cpf=VALID_CPF))
    with pytest.raises(ValueError, match="Customer already exists"):
        use_case.create_customer_only_cpf(CustomerCreateDTO(cpf=VALID_CPF))


def test_create_customer_only_cpf_rejects_invalid_cpf():
    use_case = CustomerUseCases(storage=FakeStorage(), address=FakeAddresses())
    with pytest.raises(ValidationError, match="Invalid CPF"):
        use_case.create_customer_only_cpf(CustomerCreateDTO(cpf="12345678912"))


def test_create_customer_uses_payload_address_when_city_and_state_present():
    storage = FakeStorage()
    addresses = FakeAddresses()
    use_case = CustomerUseCases(storage=storage, address=addresses)
    created = use_case.create_customer(_full_payload())
    assert created.cpf == VALID_CPF
    assert created.customer_id == 1
    assert addresses.calls == []
    assert CEP in storage.addresses
    assert storage.addresses[CEP].city == "São Paulo"
    assert storage.people[VALID_CPF].complete_name == "Andrey Murari"
    assert storage.person_addresses[0].number == "100"
    assert storage.person_addresses[0].cep_id == CEP


def test_create_customer_fetches_viacep_when_city_and_state_omitted():
    storage = FakeStorage()
    addresses = FakeAddresses()
    use_case = CustomerUseCases(storage=storage, address=addresses)
    payload = CustomerFullCreateDTO(
        cpf=VALID_CPF,
        complete_name="Andrey Murari",
        address=AddressInputDTO(cep_id=CEP),
        person_address=PersonAddressCreateDTO(number="50"),
    )
    created = use_case.create_customer(payload)
    assert created.cpf == VALID_CPF
    assert addresses.calls == [CEP]
    assert storage.addresses[CEP].street == "Praça da Sé"


def test_create_customer_reuses_existing_cep():
    storage = FakeStorage()
    existing = AddressDTO(
        cep_id=CEP,
        street="Rua Original",
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
    )
    storage.save_address(existing)
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    use_case.create_customer(_full_payload(street="Outra Rua"))
    assert storage.addresses[CEP].street == "Rua Original"


def test_create_customer_rejects_existing_person():
    storage = FakeStorage()
    storage.save_person(_person_dto())
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    with pytest.raises(ValueError, match="Person already exists"):
        use_case.create_customer(_full_payload())


def test_read_customer_includes_person_and_address():
    storage = FakeStorage()
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer(_full_payload())
    detail = use_case.read_customer(created.customer_id)
    assert detail.cpf == VALID_CPF
    assert detail.person is not None
    assert detail.person.complete_name == "Andrey Murari"
    assert detail.address is not None
    assert detail.address.cep_id == CEP
    assert detail.address.city == "São Paulo"
    assert detail.person_address is not None
    assert detail.person_address.number == "100"
    assert detail.person_address.complement == "apto 1"


def test_read_customer_only_cpf_includes_person_without_address():
    storage = FakeStorage()
    storage.save_person(_person_dto())
    use_case = CustomerUseCases(storage=storage, address=FakeAddresses())
    created = use_case.create_customer_only_cpf(CustomerCreateDTO(cpf=VALID_CPF))
    detail = use_case.read_customer(created.customer_id)
    assert detail.person is not None
    assert detail.person.complete_name == "Andrey Murari"
    assert detail.address is None
    assert detail.person_address is None
