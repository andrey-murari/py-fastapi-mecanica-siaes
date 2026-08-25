from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.vehicle_dto import VehicleDTO

class ForManageVehicle(ABC):
    @abstractmethod
    def create_vehicle(self, vehicle: dict) -> VehicleDTO:
        pass

    @abstractmethod
    def read_vehicle(self, vehicle_id: int) -> VehicleDTO:
        pass

    @abstractmethod
    def update_vehicle(self, vehicle_id: int, vehicle: dict) -> VehicleDTO:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> dict:
        pass