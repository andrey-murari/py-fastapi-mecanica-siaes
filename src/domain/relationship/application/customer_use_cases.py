from typing import override

from pydantic import ValidationError

from src.domain.relationship.entities.address import Address
from src.domain.relationship.entities.customer import Customer
from src.domain.relationship.entities.person import Person, PersonAddress
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    AddressInputDTO,
    CustomerAddressDTO,
    CustomerCreateDTO,
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerPersonDTO,
    CustomerUpdateDTO,
    CustomerVehicleDTO,
    PersonAddressDTO,
    PersonDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class CustomerUseCases(ForManageCustomer):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData, address: ForGetAddress) -> None:
        self._storage = storage
        self._address = address

    @override
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        person = Person(
            cpf=customer.cpf,
            complete_name=customer.complete_name,
            user_id=customer.user_id,
            user_modification_id=customer.user_modification_id,
            flag_active=customer.flag_active,
        )
        if self._storage.get_person(person.cpf) is not None:
            raise ValueError("Person already exists")
        if self._storage.get_customer_by_cpf(person.cpf) is not None:
            raise ValueError("Customer already exists")

        address = self._resolve_address(customer.address)
        person_address = PersonAddress(
            cpf=person.cpf,
            cep_id=address.cep_id,
            number=customer.person_address.number,
            complement=customer.person_address.complement,
            user_modification_id=customer.user_modification_id,
            flag_active=customer.flag_active,
        )
        customer_entity = Customer(cpf=person.cpf, flag_active=customer.flag_active)
        return self._storage.save_new_customer_registration(
            address=AddressDTO.model_validate(address),
            person=PersonDTO.model_validate(person),
            person_address=PersonAddressDTO.model_validate(person_address),
            customer=CustomerDTO.model_validate(customer_entity),
        )

    @override
    def create_customer_only_cpf(self, customer: CustomerCreateDTO) -> CustomerDTO:
        entity = Customer(cpf=customer.cpf)
        if self._storage.get_person(entity.cpf) is None:
            raise ValueError("Person not found")
        if self._storage.get_customer_by_cpf(entity.cpf) is not None:
            raise ValueError("Customer already exists")
        return self._storage.save_customer(CustomerDTO.model_validate(entity))

    @override
    def read_customer(self, customer_id: int) -> CustomerDetailDTO:
        customer = self._storage.get_customer(customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        return self._detail(customer)

    @override
    def find_customer_by_cpf(self, cpf: str) -> CustomerDetailDTO:
        try:
            customer_cpf = Customer(cpf=cpf).cpf
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        customer = self._storage.get_customer_by_cpf(customer_cpf)
        if customer is None:
            raise ValueError("Customer not found")
        return self._detail(customer)

    @override
    def update_customer(self, customer_id: int, customer: CustomerUpdateDTO) -> CustomerDTO:
        entity = self._storage.get_customer(customer_id)
        if entity is None:
            raise ValueError("Customer not found")
        updated = entity.model_copy(update=customer.model_dump(exclude_unset=True))
        saved = self._storage.save_customer(updated)
        return CustomerDTO.model_validate(saved)

    @override
    def delete_customer(self, customer_id: int) -> dict:
        if self._storage.get_customer(customer_id) is None:
            raise ValueError("Customer not found")
        self._storage.delete_customer(customer_id)
        return {"ok": True}

    @override
    def get_address_by_cep(self, cep: str) -> AddressDTO:
        return self._address.get_address_by_cep(cep)

    def _detail(self, customer: CustomerDTO) -> CustomerDetailDTO:
        person = self._storage.get_person(customer.cpf)
        return CustomerDetailDTO(
            **customer.model_dump(),
            person=None if person is None else CustomerPersonDTO.model_validate(person),
            addresses=self._addresses_for(customer.cpf),
            vehicles=self._vehicles_for(customer.customer_id),
        )

    def _addresses_for(self, cpf: str) -> list[CustomerAddressDTO]:
        details: list[CustomerAddressDTO] = []
        for link in self._storage.get_person_addresses(cpf):
            address = self._storage.get_address(link.cep_id)
            if address is None:
                continue
            details.append(
                CustomerAddressDTO.model_validate(
                    {**address.model_dump(), "person_address": link}
                )
            )
        return details

    def _vehicles_for(self, customer_id: int | None) -> list[CustomerVehicleDTO]:
        if customer_id is None:
            return []
        details: list[CustomerVehicleDTO] = []
        for link in self._storage.get_vehicle_customers_by_customer_id(customer_id):
            if link.vehicle_id is None:
                continue
            vehicle = self._storage.get_vehicle(link.vehicle_id)
            if vehicle is None:
                continue
            details.append(
                CustomerVehicleDTO.model_validate(
                    {**vehicle.model_dump(), "customer_vehicle": link}
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
