from datetime import datetime

import pytest

from src.domain.relationship.application.vehicle_use_cases import VehicleUseCases
from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerDTO,
    PersonAddressDTO,
    PersonDTO,
    VehicleCreateDTO,
    VehicleCustomerCreateDTO,
    VehicleCustomerDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData

PLATE = "ABC1D23"


def _vehicle_payload(**overrides) -> VehicleCreateDTO:
    payload = {
        "model": "Civic",
        "brand": "Honda",
        "manufacture_year": "2020",
        "model_year": "2021",
        "engine": "2.0",
        "fuel_type": FuelType.GASOLINE,
        "customer_vehicle": VehicleCustomerCreateDTO(
            customer_id=1,
            plate=PLATE,
            color="Prata",
            description="Carro do cliente",
        ),
    }
    payload.update(overrides)
    return VehicleCreateDTO(**payload)


class FakeStorage(ForStoringData):
    def __init__(self) -> None:
        self.customers: dict[int, CustomerDTO] = {}
        self.vehicles: dict[int, VehicleDTO] = {}
        self.vehicle_customers: dict[int, VehicleCustomerDTO] = {}
        self._next_vehicle_id = 1
        self._next_vehicle_customer_id = 1

    def create_db_and_tables(self) -> None:
        return None

    def close(self) -> None:
        return None

    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        return self.customers.get(customer_id)

    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        for customer in self.customers.values():
            if customer.cpf == cpf:
                return customer
        return None

    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        return customer

    def delete_customer(self, customer_id: int) -> None:
        return None

    def get_person(self, cpf: str) -> PersonDTO | None:
        return None

    def save_person(self, person: PersonDTO) -> PersonDTO:
        return person

    def get_address(self, cep_id: str) -> AddressDTO | None:
        return None

    def save_address(self, address: AddressDTO) -> AddressDTO:
        return address

    def get_person_addresses(self, cpf: str) -> list[PersonAddressDTO]:
        return []

    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        return person_address

    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        return customer

    def get_vehicle(self, vehicle_id: int) -> VehicleDTO | None:
        return self.vehicles.get(vehicle_id)

    def save_vehicle(self, vehicle: VehicleDTO) -> VehicleDTO:
        dto = VehicleDTO.model_validate(vehicle)
        if dto.vehicle_id is None:
            dto = dto.model_copy(update={"vehicle_id": self._next_vehicle_id})
            self._next_vehicle_id += 1
        self.vehicles[dto.vehicle_id] = dto
        return dto

    def delete_vehicle(self, vehicle_id: int) -> None:
        self.vehicles.pop(vehicle_id, None)
        self.vehicle_customers = {
            link_id: link
            for link_id, link in self.vehicle_customers.items()
            if link.vehicle_id != vehicle_id
        }

    def get_vehicle_customer_by_vehicle_id(self, vehicle_id: int) -> VehicleCustomerDTO | None:
        for link in self.vehicle_customers.values():
            if link.vehicle_id == vehicle_id:
                return link
        return None

    def get_vehicle_customer_by_plate(self, plate: str) -> VehicleCustomerDTO | None:
        for link in self.vehicle_customers.values():
            if link.plate == plate:
                return link
        return None

    def get_vehicle_customers_by_customer_id(self, customer_id: int) -> list[VehicleCustomerDTO]:
        return [link for link in self.vehicle_customers.values() if link.customer_id == customer_id]

    def save_vehicle_customer(self, vehicle_customer: VehicleCustomerDTO) -> VehicleCustomerDTO:
        dto = VehicleCustomerDTO.model_validate(vehicle_customer)
        if dto.vehicle_customer_id is None:
            dto = dto.model_copy(update={"vehicle_customer_id": self._next_vehicle_customer_id})
            self._next_vehicle_customer_id += 1
        self.vehicle_customers[dto.vehicle_customer_id] = dto
        return dto

    def save_new_vehicle_registration(
        self,
        vehicle: VehicleDTO,
        vehicle_customer: VehicleCustomerDTO,
    ) -> VehicleDTO:
        saved = self.save_vehicle(vehicle)
        self.save_vehicle_customer(
            vehicle_customer.model_copy(update={"vehicle_id": saved.vehicle_id})
        )
        return saved

    def get_order(self, order_id: int):
        return None

    def save_order(self, order):
        return order

    def delete_order(self, order_id: int) -> None:
        return None

    def save_service(self, service):
        return service

    def delete_service(self, service_id: int) -> None:
        return None

    def get_service(self, service_id: int):
        return None

    def seed_customer(self, customer_id: int = 1) -> None:
        self.customers[customer_id] = CustomerDTO(
            customer_id=customer_id,
            cpf="52998224725",
            insertion_date=datetime.now(),
        )


def test_create_vehicle_requires_existing_customer():
    use_case = VehicleUseCases(storage=FakeStorage())
    with pytest.raises(ValueError, match="Customer not found"):
        use_case.create_vehicle(_vehicle_payload())


def test_create_vehicle_saves_vehicle_and_customer_vehicle():
    storage = FakeStorage()
    storage.seed_customer()
    created = VehicleUseCases(storage=storage).create_vehicle(_vehicle_payload())
    assert created.vehicle_id == 1
    assert created.model == "Civic"
    assert created.brand == "Honda"
    assert created.fuel_type == FuelType.GASOLINE
    link = storage.get_vehicle_customer_by_vehicle_id(1)
    assert link is not None
    assert link.customer_id == 1
    assert link.plate == PLATE
    assert link.color == "Prata"


def test_create_vehicle_rejects_duplicate_plate():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    use_case.create_vehicle(_vehicle_payload())
    with pytest.raises(ValueError, match="Plate already exists"):
        use_case.create_vehicle(_vehicle_payload())


def test_create_vehicle_normalizes_plate():
    storage = FakeStorage()
    storage.seed_customer()
    created = VehicleUseCases(storage=storage).create_vehicle(
        _vehicle_payload(
            customer_vehicle=VehicleCustomerCreateDTO(
                customer_id=1,
                plate="abc1d23",
                color="Preto",
            )
        )
    )
    link = storage.get_vehicle_customer_by_vehicle_id(created.vehicle_id)
    assert link is not None
    assert link.plate == "ABC1D23"


def test_create_vehicle_rejects_invalid_plate():
    storage = FakeStorage()
    storage.seed_customer()
    with pytest.raises(ValueError, match="Invalid plate"):
        VehicleUseCases(storage=storage).create_vehicle(
            _vehicle_payload(
                customer_vehicle=VehicleCustomerCreateDTO(
                    customer_id=1,
                    plate="INVALID",
                    color="Preto",
                )
            )
        )


def test_create_vehicle_rejects_manufacture_year_after_model_year():
    storage = FakeStorage()
    storage.seed_customer()
    with pytest.raises(ValueError, match="Manufacture year cannot be after model year"):
        VehicleUseCases(storage=storage).create_vehicle(
            _vehicle_payload(manufacture_year="2022", model_year="2021")
        )


def test_read_vehicle_includes_customer_vehicle():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    created = use_case.create_vehicle(_vehicle_payload())
    detail = use_case.read_vehicle(created.vehicle_id)
    assert detail.model == "Civic"
    assert detail.customer_vehicle is not None
    assert detail.customer_vehicle.plate == PLATE
    assert detail.customer_vehicle.customer_id == 1


def test_read_vehicle_not_found():
    with pytest.raises(ValueError, match="Vehicle not found"):
        VehicleUseCases(storage=FakeStorage()).read_vehicle(99)


def test_update_vehicle_changes_model_and_plate():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    created = use_case.create_vehicle(_vehicle_payload())
    updated = use_case.update_vehicle(
        created.vehicle_id,
        VehicleUpdateDTO(model="City", plate="XYZ1A23"),
    )
    assert updated.model == "City"
    link = storage.get_vehicle_customer_by_vehicle_id(created.vehicle_id)
    assert link is not None
    assert link.plate == "XYZ1A23"


def test_update_vehicle_rejects_duplicate_plate():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    first = use_case.create_vehicle(_vehicle_payload())
    use_case.create_vehicle(
        _vehicle_payload(
            customer_vehicle=VehicleCustomerCreateDTO(
                customer_id=1,
                plate="XYZ1A23",
                color="Preto",
            )
        )
    )
    with pytest.raises(ValueError, match="Plate already exists"):
        use_case.update_vehicle(first.vehicle_id, VehicleUpdateDTO(plate="XYZ1A23"))


def test_delete_vehicle():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    created = use_case.create_vehicle(_vehicle_payload())
    assert use_case.delete_vehicle(created.vehicle_id) == {"ok": True}
    assert storage.get_vehicle(created.vehicle_id) is None
    assert storage.get_vehicle_customer_by_vehicle_id(created.vehicle_id) is None


def test_find_vehicles_by_customer_cpf():
    storage = FakeStorage()
    storage.seed_customer()
    use_case = VehicleUseCases(storage=storage)
    use_case.create_vehicle(_vehicle_payload())
    use_case.create_vehicle(
        _vehicle_payload(
            customer_vehicle=VehicleCustomerCreateDTO(
                customer_id=1,
                plate="XYZ1A23",
                color="Preto",
            )
        )
    )
    found = use_case.find_vehicles_by_customer_cpf("52998224725")
    assert len(found) == 2
    assert {item.customer_vehicle.plate for item in found if item.customer_vehicle} == {
        "ABC1D23",
        "XYZ1A23",
    }


def test_find_vehicles_by_customer_cpf_returns_empty_when_no_vehicles():
    storage = FakeStorage()
    storage.seed_customer()
    assert VehicleUseCases(storage=storage).find_vehicles_by_customer_cpf("52998224725") == []


def test_find_vehicles_by_customer_cpf_requires_customer():
    with pytest.raises(ValueError, match="Customer not found"):
        VehicleUseCases(storage=FakeStorage()).find_vehicles_by_customer_cpf("52998224725")


def test_find_vehicles_by_customer_cpf_rejects_invalid_cpf():
    with pytest.raises(ValueError, match="Invalid CPF"):
        VehicleUseCases(storage=FakeStorage()).find_vehicles_by_customer_cpf("12345678912")
