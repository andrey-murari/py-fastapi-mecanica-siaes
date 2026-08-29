from typing import override

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
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class InMemoryStorage(ForStoringData):
    """Driven port test double: same contract, dictionaries instead of SQLAlchemy."""

    def __init__(self) -> None:
        self.customers: dict[int, CustomerDTO] = {}
        self.people: dict[str, PersonDTO] = {}
        self.addresses: dict[str, AddressDTO] = {}
        self.person_addresses: list[PersonAddressDTO] = []
        self.contacts: dict[int, PersonContactDTO] = {}
        self.vehicles: dict[int, VehicleDTO] = {}
        self.vehicle_customers: dict[int, VehicleCustomerDTO] = {}
        self.users: dict[int, UserDTO] = {}
        self.services: dict[int, ServiceDTO] = {}
        self.parts: dict[int, PartDTO] = {}
        self.orders: dict[int, ServiceOrderDTO] = {}
        self.order_service_lines: dict[int, OrderServiceLineDTO] = {}
        self.order_part_lines: dict[int, OrderPartLineDTO] = {}
        self.stock_operations: dict[int, StockOperationDTO] = {}
        self._sequences: dict[str, int] = {}

    def _next_id(self, sequence: str) -> int:
        self._sequences[sequence] = self._sequences.get(sequence, 0) + 1
        return self._sequences[sequence]

    @override
    def create_db_and_tables(self) -> None:
        return None

    @override
    def close(self) -> None:
        return None

    @override
    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        return self.customers.get(customer_id)

    @override
    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        return next(
            (customer for customer in self.customers.values() if customer.cpf == cpf),
            None,
        )

    @override
    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        customer_id = customer.customer_id or self._next_id("customer")
        stored = customer.model_copy(update={"customer_id": customer_id})
        self.customers[customer_id] = stored
        return stored

    @override
    def delete_customer(self, customer_id: int) -> None:
        self.customers.pop(customer_id, None)

    @override
    def get_person(self, cpf: str) -> PersonDTO | None:
        return self.people.get(cpf)

    @override
    def save_person(self, person: PersonDTO) -> PersonDTO:
        self.people[person.cpf] = person
        return person

    @override
    def delete_person(self, cpf: str) -> None:
        self.people.pop(cpf, None)
        self.person_addresses = [item for item in self.person_addresses if item.cpf != cpf]
        for contact_id, contact in list(self.contacts.items()):
            if contact.cpf == cpf:
                self.contacts.pop(contact_id)

    @override
    def get_contact(self, contact_id: int) -> PersonContactDTO | None:
        return self.contacts.get(contact_id)

    @override
    def get_contacts_by_cpf(self, cpf: str) -> list[PersonContactDTO]:
        return [contact for contact in self.contacts.values() if contact.cpf == cpf]

    @override
    def save_contact(self, contact: PersonContactDTO) -> PersonContactDTO:
        contact_id = contact.contact_id or self._next_id("contact")
        stored = contact.model_copy(update={"contact_id": contact_id})
        self.contacts[contact_id] = stored
        return stored

    @override
    def delete_contact(self, contact_id: int) -> None:
        self.contacts.pop(contact_id, None)

    @override
    def get_address(self, cep_id: str) -> AddressDTO | None:
        return self.addresses.get(cep_id)

    @override
    def save_address(self, address: AddressDTO) -> AddressDTO:
        self.addresses[address.cep_id] = address
        return address

    @override
    def get_person_addresses(self, cpf: str) -> list[PersonAddressDTO]:
        return [item for item in self.person_addresses if item.cpf == cpf]

    @override
    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        self.person_addresses.append(person_address)
        return person_address

    @override
    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        self.save_address(address)
        self.save_person(person)
        self.save_person_address(person_address)
        return self.save_customer(customer)

    @override
    def get_vehicle(self, vehicle_id: int) -> VehicleDTO | None:
        return self.vehicles.get(vehicle_id)

    @override
    def save_vehicle(self, vehicle: VehicleDTO) -> VehicleDTO:
        vehicle_id = vehicle.vehicle_id or self._next_id("vehicle")
        stored = vehicle.model_copy(update={"vehicle_id": vehicle_id})
        self.vehicles[vehicle_id] = stored
        return stored

    @override
    def delete_vehicle(self, vehicle_id: int) -> None:
        self.vehicles.pop(vehicle_id, None)
        for link_id, link in list(self.vehicle_customers.items()):
            if link.vehicle_id == vehicle_id:
                self.vehicle_customers.pop(link_id)

    @override
    def get_vehicle_customer(self, vehicle_customer_id: int) -> VehicleCustomerDTO | None:
        return self.vehicle_customers.get(vehicle_customer_id)

    @override
    def get_vehicle_customer_by_vehicle_id(self, vehicle_id: int) -> VehicleCustomerDTO | None:
        return next(
            (link for link in self.vehicle_customers.values() if link.vehicle_id == vehicle_id),
            None,
        )

    @override
    def get_vehicle_customer_by_plate(self, plate: str) -> VehicleCustomerDTO | None:
        return next(
            (link for link in self.vehicle_customers.values() if link.plate == plate),
            None,
        )

    @override
    def get_vehicle_customers_by_customer_id(self, customer_id: int) -> list[VehicleCustomerDTO]:
        return [
            link for link in self.vehicle_customers.values() if link.customer_id == customer_id
        ]

    @override
    def save_vehicle_customer(self, vehicle_customer: VehicleCustomerDTO) -> VehicleCustomerDTO:
        link_id = vehicle_customer.vehicle_customer_id or self._next_id("vehicle_customer")
        stored = vehicle_customer.model_copy(update={"vehicle_customer_id": link_id})
        self.vehicle_customers[link_id] = stored
        return stored

    @override
    def save_new_vehicle_registration(
        self,
        vehicle: VehicleDTO,
        vehicle_customer: VehicleCustomerDTO,
    ) -> VehicleDTO:
        stored_vehicle = self.save_vehicle(vehicle)
        self.save_vehicle_customer(
            vehicle_customer.model_copy(update={"vehicle_id": stored_vehicle.vehicle_id})
        )
        return stored_vehicle

    @override
    def get_user(self, user_id: int) -> UserDTO | None:
        return self.users.get(user_id)

    @override
    def save_user(self, user: UserDTO) -> UserDTO:
        user_id = user.user_id or self._next_id("user")
        stored = user.model_copy(update={"user_id": user_id})
        self.users[user_id] = stored
        return stored

    @override
    def get_service(self, service_id: int) -> ServiceDTO | None:
        return self.services.get(service_id)

    @override
    def save_service(self, service: ServiceDTO) -> ServiceDTO:
        service_id = service.service_id or self._next_id("service")
        stored = service.model_copy(update={"service_id": service_id})
        self.services[service_id] = stored
        return stored

    @override
    def delete_service(self, service_id: int) -> None:
        self.services.pop(service_id, None)

    @override
    def get_part(self, part_id: int) -> PartDTO | None:
        return self.parts.get(part_id)

    @override
    def save_part(self, part: PartDTO) -> PartDTO:
        part_id = part.part_id or self._next_id("part")
        stored = part.model_copy(update={"part_id": part_id})
        self.parts[part_id] = stored
        return stored

    @override
    def delete_part(self, part_id: int) -> None:
        self.parts.pop(part_id, None)

    @override
    def get_service_order(self, order_id: int) -> ServiceOrderDTO | None:
        return self.orders.get(order_id)

    @override
    def save_service_order(self, order: ServiceOrderDTO) -> ServiceOrderDTO:
        order_id = order.order_id or self._next_id("order")
        stored = order.model_copy(update={"order_id": order_id})
        self.orders[order_id] = stored
        return stored

    @override
    def delete_service_order(self, order_id: int) -> None:
        self.orders.pop(order_id, None)
        self.replace_order_lines(order_id=order_id, service_lines=[], part_lines=[])

    @override
    def get_order_service_lines(self, order_id: int) -> list[OrderServiceLineDTO]:
        return [line for line in self.order_service_lines.values() if line.order_id == order_id]

    @override
    def get_order_part_lines(self, order_id: int) -> list[OrderPartLineDTO]:
        return [line for line in self.order_part_lines.values() if line.order_id == order_id]

    @override
    def save_order_service_line(self, line: OrderServiceLineDTO) -> OrderServiceLineDTO:
        line_id = line.order_service_id or self._next_id("order_service")
        stored = line.model_copy(update={"order_service_id": line_id})
        self.order_service_lines[line_id] = stored
        return stored

    def _save_order_part_line(self, line: OrderPartLineDTO) -> OrderPartLineDTO:
        line_id = line.order_part_id or self._next_id("order_part")
        stored = line.model_copy(update={"order_part_id": line_id})
        self.order_part_lines[line_id] = stored
        return stored

    @override
    def save_new_service_order(
        self,
        order: ServiceOrderDTO,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> ServiceOrderDTO:
        stored = self.save_service_order(order)
        self.replace_order_lines(
            order_id=stored.order_id or 0,
            service_lines=service_lines,
            part_lines=part_lines,
        )
        return stored

    @override
    def replace_order_lines(
        self,
        order_id: int,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> None:
        for line_id, line in list(self.order_service_lines.items()):
            if line.order_id == order_id:
                self.order_service_lines.pop(line_id)
        for line_id, line in list(self.order_part_lines.items()):
            if line.order_id == order_id:
                self.order_part_lines.pop(line_id)
        for line in service_lines:
            self.save_order_service_line(
                line.model_copy(update={"order_service_id": None, "order_id": order_id})
            )
        for line in part_lines:
            self._save_order_part_line(
                line.model_copy(update={"order_part_id": None, "order_id": order_id})
            )

    @override
    def get_order_part_line(self, order_part_id: int) -> OrderPartLineDTO | None:
        return self.order_part_lines.get(order_part_id)

    @override
    def get_stock_operations_by_part_id(self, part_id: int) -> list[StockOperationDTO]:
        return [
            operation
            for operation in self.stock_operations.values()
            if operation.part_id == part_id
        ]

    @override
    def get_stock_operation_by_order_part_id(
        self,
        order_part_id: int,
    ) -> StockOperationDTO | None:
        return next(
            (
                operation
                for operation in self.stock_operations.values()
                if operation.order_part_id == order_part_id
            ),
            None,
        )

    @override
    def apply_stock_operation(
        self,
        operation: StockOperationDTO,
        updated_part: PartDTO,
    ) -> StockOperationDTO:
        self.save_part(updated_part)
        operation_id = operation.operation_id or self._next_id("stock_operation")
        stored = operation.model_copy(update={"operation_id": operation_id})
        self.stock_operations[operation_id] = stored
        return stored
