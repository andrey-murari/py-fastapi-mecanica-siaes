from typing import override

from pydantic import ValidationError

from src.domain.relationship.entities.customer import Customer
from src.domain.relationship.entities.vehicle import Vehicle, VehicleCustomer
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleCustomerDTO,
    VehicleDetailDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class VehicleUseCases(ForManageVehicle):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_vehicle(self, vehicle: VehicleCreateDTO) -> VehicleDTO:
        if self._storage.get_customer(vehicle.customer_vehicle.customer_id) is None:
            raise ValueError("Customer not found")
        try:
            vehicle_entity = Vehicle(
                model=vehicle.model,
                brand=vehicle.brand,
                manufacture_year=vehicle.manufacture_year,
                model_year=vehicle.model_year,
                engine=vehicle.engine,
                fuel_type=vehicle.fuel_type,
                flag_active=vehicle.flag_active,
            )
            customer_vehicle = VehicleCustomer(
                customer_id=vehicle.customer_vehicle.customer_id,
                plate=vehicle.customer_vehicle.plate,
                color=vehicle.customer_vehicle.color,
                description=vehicle.customer_vehicle.description,
                user_modification_id=vehicle.customer_vehicle.user_modification_id,
                flag_active=vehicle.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if self._storage.get_vehicle_customer_by_plate(customer_vehicle.plate) is not None:
            raise ValueError("Plate already exists")
        return self._storage.save_new_vehicle_registration(
            vehicle=VehicleDTO.model_validate(vehicle_entity),
            vehicle_customer=VehicleCustomerDTO.model_validate(customer_vehicle),
        )

    @override
    def read_vehicle(self, vehicle_id: int) -> VehicleDetailDTO:
        vehicle = self._storage.get_vehicle(vehicle_id)
        if vehicle is None:
            raise ValueError("Vehicle not found")
        return VehicleDetailDTO(
            **vehicle.model_dump(),
            customer_vehicle=self._storage.get_vehicle_customer_by_vehicle_id(vehicle_id),
        )

    @override
    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdateDTO) -> VehicleDTO:
        entity = self._storage.get_vehicle(vehicle_id)
        if entity is None:
            raise ValueError("Vehicle not found")
        vehicle_fields = vehicle.model_dump(
            exclude_unset=True,
            exclude={"plate", "color", "description"},
        )
        try:
            updated_vehicle = Vehicle.model_validate(entity.model_copy(update=vehicle_fields))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        saved = self._storage.save_vehicle(VehicleDTO.model_validate(updated_vehicle))

        link_fields = vehicle.model_dump(
            exclude_unset=True,
            include={"plate", "color", "description", "flag_active"},
        )
        if link_fields:
            link = self._storage.get_vehicle_customer_by_vehicle_id(vehicle_id)
            if link is not None:
                try:
                    candidate = VehicleCustomer.model_validate(link.model_copy(update=link_fields))
                except ValidationError as exc:
                    raise value_error_from(exc) from exc
                if "plate" in link_fields:
                    existing = self._storage.get_vehicle_customer_by_plate(candidate.plate)
                    if (
                        existing is not None
                        and existing.vehicle_customer_id != link.vehicle_customer_id
                    ):
                        raise ValueError("Plate already exists")
                self._storage.save_vehicle_customer(VehicleCustomerDTO.model_validate(candidate))
        return saved

    @override
    def delete_vehicle(self, vehicle_id: int) -> dict:
        if self._storage.get_vehicle(vehicle_id) is None:
            raise ValueError("Vehicle not found")
        self._storage.delete_vehicle(vehicle_id)
        return {"ok": True}

    @override
    def find_vehicles_by_customer_cpf(self, cpf: str) -> list[VehicleDetailDTO]:
        try:
            customer_cpf = Customer(cpf=cpf).cpf
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        customer = self._storage.get_customer_by_cpf(customer_cpf)
        if customer is None or customer.customer_id is None:
            raise ValueError("Customer not found")
        details: list[VehicleDetailDTO] = []
        for link in self._storage.get_vehicle_customers_by_customer_id(customer.customer_id):
            if link.vehicle_id is None:
                continue
            vehicle = self._storage.get_vehicle(link.vehicle_id)
            if vehicle is None:
                continue
            details.append(
                VehicleDetailDTO(**vehicle.model_dump(), customer_vehicle=link)
            )
        return details
