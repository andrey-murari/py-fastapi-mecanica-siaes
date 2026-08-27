from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerDTO,
    PersonAddressDTO,
    PersonDTO,
    VehicleCustomerDTO,
    VehicleDTO,
)
from src.ports.driver.for_manage_services.dto.service_dto import ServiceDTO


class ForStoringData(ABC):
    """Driven port: persistence. The application never sees SQLAlchemy."""

    @abstractmethod
    def create_db_and_tables(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        pass

    @abstractmethod
    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        pass

    @abstractmethod
    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> None:
        pass

    @abstractmethod
    def get_person(self, cpf: str) -> PersonDTO | None:
        pass

    @abstractmethod
    def save_person(self, person: PersonDTO) -> PersonDTO:
        pass

    @abstractmethod
    def get_address(self, cep_id: str) -> AddressDTO | None:
        pass

    @abstractmethod
    def save_address(self, address: AddressDTO) -> AddressDTO:
        pass

    @abstractmethod
    def get_person_addresses(self, cpf: str) -> list[PersonAddressDTO]:
        pass

    @abstractmethod
    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        pass

    @abstractmethod
    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        pass

    @abstractmethod
    def get_vehicle(self, vehicle_id: int) -> VehicleDTO | None:
        pass

    @abstractmethod
    def save_vehicle(self, vehicle: VehicleDTO) -> VehicleDTO:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> None:
        pass

    @abstractmethod
    def get_vehicle_customer_by_vehicle_id(self, vehicle_id: int) -> VehicleCustomerDTO | None:
        pass

    @abstractmethod
    def get_vehicle_customer_by_plate(self, plate: str) -> VehicleCustomerDTO | None:
        pass

    @abstractmethod
    def get_vehicle_customers_by_customer_id(self, customer_id: int) -> list[VehicleCustomerDTO]:
        pass

    @abstractmethod
    def save_vehicle_customer(self, vehicle_customer: VehicleCustomerDTO) -> VehicleCustomerDTO:
        pass

    @abstractmethod
    def save_new_vehicle_registration(
        self,
        vehicle: VehicleDTO,
        vehicle_customer: VehicleCustomerDTO,
    ) -> VehicleDTO:
        pass

    @abstractmethod
    def get_order(self, order_id: int):
        pass

    @abstractmethod
    def save_order(self, order: OrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def delete_order(self, order_id: int) -> None:
        pass

    @abstractmethod
    def save_service(self, service: ServiceDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def delete_service(self, service_id: int) -> None:
        pass

    @abstractmethod
    def get_service(self, service_id: int) -> ServiceDTO | None:
        pass
    
    