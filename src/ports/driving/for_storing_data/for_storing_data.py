from abc import ABC, abstractmethod

from src.ports.driver.for_manage_inventory.dto.inventory_dto import StockOperationDTO
from src.ports.driver.for_manage_parts.dto.part_dto import PartDTO
from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerDTO,
    PersonAddressDTO,
    PersonContactDTO,
    PersonDTO,
    UserDTO,
    VehicleCustomerDTO,
    VehicleDTO,
)
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    OrderPartLineDTO,
    OrderServiceLineDTO,
    ServiceOrderDTO,
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
    def delete_person(self, cpf: str) -> None:
        pass

    @abstractmethod
    def get_contact(self, contact_id: int) -> PersonContactDTO | None:
        pass

    @abstractmethod
    def get_contacts_by_cpf(self, cpf: str) -> list[PersonContactDTO]:
        pass

    @abstractmethod
    def save_contact(self, contact: PersonContactDTO) -> PersonContactDTO:
        pass

    @abstractmethod
    def delete_contact(self, contact_id: int) -> None:
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
    def get_vehicle_customer(self, vehicle_customer_id: int) -> VehicleCustomerDTO | None:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> UserDTO | None:
        pass

    @abstractmethod
    def save_user(self, user: UserDTO) -> UserDTO:
        pass

    @abstractmethod
    def get_service(self, service_id: int) -> ServiceDTO | None:
        pass

    @abstractmethod
    def save_service(self, service: ServiceDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def delete_service(self, service_id: int) -> None:
        pass

    @abstractmethod
    def get_part(self, part_id: int) -> PartDTO | None:
        pass

    @abstractmethod
    def save_part(self, part: PartDTO) -> PartDTO:
        pass

    @abstractmethod
    def delete_part(self, part_id: int) -> None:
        pass

    @abstractmethod
    def get_service_order(self, order_id: int) -> ServiceOrderDTO | None:
        pass

    @abstractmethod
    def save_service_order(self, order: ServiceOrderDTO) -> ServiceOrderDTO:
        pass

    @abstractmethod
    def delete_service_order(self, order_id: int) -> None:
        pass

    @abstractmethod
    def get_order_service_lines(self, order_id: int) -> list[OrderServiceLineDTO]:
        pass

    @abstractmethod
    def get_order_part_lines(self, order_id: int) -> list[OrderPartLineDTO]:
        pass

    @abstractmethod
    def save_order_service_line(self, line: OrderServiceLineDTO) -> OrderServiceLineDTO:
        pass

    @abstractmethod
    def save_new_service_order(
        self,
        order: ServiceOrderDTO,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> ServiceOrderDTO:
        pass

    @abstractmethod
    def replace_order_lines(
        self,
        order_id: int,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> None:
        pass

    @abstractmethod
    def get_order_part_line(self, order_part_id: int) -> OrderPartLineDTO | None:
        pass

    @abstractmethod
    def get_stock_operations_by_part_id(self, part_id: int) -> list[StockOperationDTO]:
        pass

    @abstractmethod
    def get_stock_operation_by_order_part_id(
        self,
        order_part_id: int,
    ) -> StockOperationDTO | None:
        pass

    @abstractmethod
    def apply_stock_operation(
        self,
        operation: StockOperationDTO,
        updated_part: PartDTO,
    ) -> StockOperationDTO:
        pass
