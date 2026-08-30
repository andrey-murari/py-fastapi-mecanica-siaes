from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)


class ForManageVehicle(ABC):
    @abstractmethod
    def create_vehicle(self, vehicle: VehicleCreateDTO) -> VehicleDTO:
        pass

    @abstractmethod
    def read_vehicle(self, vehicle_id: int) -> VehicleDTO:
        pass

    @abstractmethod
    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdateDTO) -> VehicleDTO:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> dict:
        pass

    @abstractmethod
    def find_vehicles_by_person_id(self, person_id: str) -> list[VehicleDTO]:
        pass
