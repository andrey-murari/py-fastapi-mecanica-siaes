from typing import override

from pydantic import ValidationError

from src.domain.relationship.entities.person import Person
from src.domain.relationship.entities.vehicle import Vehicle
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
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
        self._require_customer(vehicle.person_id)
        try:
            entity = Vehicle(
                person_id=vehicle.person_id,
                model=vehicle.model,
                brand=vehicle.brand,
                manufacture_year=vehicle.manufacture_year,
                model_year=vehicle.model_year,
                engine=vehicle.engine,
                fuel_type=vehicle.fuel_type,
                plate=vehicle.plate,
                color=vehicle.color,
                description=vehicle.description,
                user_modification_id=vehicle.user_modification_id,
                flag_active=vehicle.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if self._storage.get_vehicle_by_plate(entity.plate) is not None:
            raise ValueError("Plate already exists")
        return self._storage.save_vehicle(VehicleDTO.model_validate(entity))

    @override
    def read_vehicle(self, vehicle_id: int) -> VehicleDTO:
        return self._require_vehicle(vehicle_id)

    @override
    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdateDTO) -> VehicleDTO:
        stored = self._require_vehicle(vehicle_id)
        changes = vehicle.model_dump(exclude_unset=True)
        try:
            updated = Vehicle.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if "plate" in changes:
            existing = self._storage.get_vehicle_by_plate(updated.plate)
            if existing is not None and existing.vehicle_id != vehicle_id:
                raise ValueError("Plate already exists")
        return self._storage.save_vehicle(VehicleDTO.model_validate(updated))

    @override
    def delete_vehicle(self, vehicle_id: int) -> dict:
        self._require_vehicle(vehicle_id)
        self._storage.delete_vehicle(vehicle_id)
        return {"ok": True}

    @override
    def find_vehicles_by_person_id(self, person_id: str) -> list[VehicleDTO]:
        customer = self._require_customer(person_id)
        return self._storage.get_vehicles_by_person_id(customer)

    def _require_vehicle(self, vehicle_id: int) -> VehicleDTO:
        vehicle = self._storage.get_vehicle(vehicle_id)
        if vehicle is None:
            raise ValueError("Vehicle not found")
        return vehicle

    def _require_customer(self, person_id: str) -> str:
        validated = Person.validate_person_id(person_id)
        person = self._storage.get_person(validated)
        if person is None:
            raise ValueError("Person not found")
        if not person.flag_customer:
            raise ValueError("Person is not a customer")
        return validated
