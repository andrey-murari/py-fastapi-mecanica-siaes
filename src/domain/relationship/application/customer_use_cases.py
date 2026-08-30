from typing import override

from pydantic import ValidationError

from src.domain.relationship.application.person_login import create_login_for_person
from src.domain.relationship.entities.address import Address
from src.domain.relationship.entities.person import Person, PersonAddress
from src.domain.relationship.value_objects.user_type import UserType
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    AddressInputDTO,
    CustomerAddressDTO,
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
    CustomerVehicleDTO,
    PersonAddressDTO,
    PersonDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class CustomerUseCases(ForManageCustomer):
    """Drives person registration from the customer angle: person, address and the customer flag."""

    def __init__(self, storage: ForStoringData, address: ForGetAddress) -> None:
        self._storage = storage
        self._address = address

    @override
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        try:
            person = Person(
                person_id=customer.person_id,
                complete_name=customer.complete_name,
                user_modification_id=customer.user_modification_id,
                flag_customer=True,
                flag_active=customer.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if self._storage.get_person(person.person_id) is not None:
            raise ValueError("Person already exists")
        account = create_login_for_person(
            self._storage,
            person.person_id,
            person.complete_name,
            UserType.CLIENT,
            customer.user_modification_id,
        )
        person = person.model_copy(update={"user_id": account.user_id})

        address = self._resolve_address(customer.address)
        try:
            person_address = PersonAddress(
                person_id=person.person_id,
                cep_id=address.cep_id,
                number=customer.person_address.number,
                complement=customer.person_address.complement,
                user_modification_id=customer.user_modification_id,
                flag_active=customer.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        saved = self._storage.save_new_customer_registration(
            address=AddressDTO.model_validate(address),
            person=PersonDTO.model_validate(person),
            person_address=PersonAddressDTO.model_validate(person_address),
        )
        return CustomerDTO.model_validate(saved)

    @override
    def read_customer(self, person_id: str) -> CustomerDetailDTO:
        return self._detail(self._require_customer(person_id))

    @override
    def update_customer(self, person_id: str, customer: CustomerUpdateDTO) -> CustomerDTO:
        stored = self._require_customer(person_id)
        changes = customer.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = Person.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        saved = self._storage.save_person(PersonDTO.model_validate(updated))
        return CustomerDTO.model_validate(saved)

    @override
    def delete_customer(self, person_id: str) -> dict:
        customer = self._require_customer(person_id)
        if self._storage.get_vehicles_by_person_id(customer.person_id):
            raise ValueError("Person has vehicles")
        self._storage.delete_person(customer.person_id)
        return {"ok": True}

    def _require_customer(self, person_id: str) -> PersonDTO:
        try:
            validated = Person.validate_person_id(person_id)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        person = self._storage.get_person(validated)
        if person is None or not person.flag_customer:
            raise ValueError("Customer not found")
        return person

    def _detail(self, customer: PersonDTO) -> CustomerDetailDTO:
        return CustomerDetailDTO(
            **customer.model_dump(),
            addresses=self._addresses_for(customer.person_id),
            vehicles=[
                CustomerVehicleDTO.model_validate(vehicle)
                for vehicle in self._storage.get_vehicles_by_person_id(customer.person_id)
            ],
        )

    def _addresses_for(self, person_id: str) -> list[CustomerAddressDTO]:
        details: list[CustomerAddressDTO] = []
        for link in self._storage.get_person_addresses(person_id):
            address = self._storage.get_address(link.cep_id)
            if address is None:
                continue
            details.append(
                CustomerAddressDTO.model_validate(
                    {**address.model_dump(), "person_address": link}
                )
            )
        return details

    def _resolve_address(self, address_input: AddressInputDTO) -> Address:
        if address_input.city and address_input.state:
            return Address(
                cep_id=address_input.cep_id,
                street=address_input.street or "",
                neighborhood=address_input.neighborhood or "",
                city=address_input.city,
                state=address_input.state,
            )
        dto = self._address.get_address_by_cep(address_input.cep_id)
        return Address.model_validate(dto)
