from typing import Any, override
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

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

DEFAULT_ENGINE = os.getenv("FOR_STORING_DATA") or "sqlite"
DEFAULT_SQLITE_URL = "sqlite:///database.db"


class Base(DeclarativeBase):
    ...


def _connect_args(engine_name: str) -> dict:
    if engine_name == "sqlite":
        return {"check_same_thread": False}
    if engine_name == "mysql":
        return {}
    raise ValueError(f"Invalid database: {engine_name}")


def _database_url(engine_name: str) -> str:
    env_url = os.getenv(f"{engine_name.upper()}_URL")
    if env_url:
        return env_url
    if engine_name == "sqlite":
        return DEFAULT_SQLITE_URL
    raise ValueError(f"Missing {engine_name.upper()}_URL")


def _dump(model: Any, *, exclude_id: str | None = None) -> dict[str, Any]:
    payload = model.model_dump() if hasattr(model, "model_dump") else dict(model)
    if exclude_id and payload.get(exclude_id) is None:
        payload.pop(exclude_id, None)
    return payload


class RdbmsAdapter(ForStoringData):
    def __init__(self, echo: bool = False) -> None:
        self.engine_name = DEFAULT_ENGINE
        self.url = _database_url(self.engine_name)
        self.engine = create_engine(
            self.url,
            echo=echo,
            connect_args=_connect_args(self.engine_name),
        )
        self.session_local = sessionmaker(bind=self.engine, class_=Session)

    def _import_models(self) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models import (  # noqa: F401
            address_repository,
            contacts_repository,
            customer_repository,
            order_part_repository,
            order_service_repository,
            part_repository,
            person_address_repository,
            person_repository,
            service_order_repository,
            service_repository,
            stock_operation_repository,
            user_repository,
            vehicle_customer_repository,
            vehicles_repository,
        )

    @override
    def create_db_and_tables(self) -> None:
        self._import_models()
        Base.metadata.create_all(bind=self.engine)

    @override
    def close(self) -> None:
        self.engine.dispose()

    @override
    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.customer_repository import (
            CustomerRepository,
        )

        with self.session_local() as session:
            row = session.get(CustomerRepository, customer_id)
            return None if row is None else CustomerDTO.model_validate(row)

    @override
    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.customer_repository import (
            CustomerRepository,
        )

        with self.session_local() as session:
            row = session.scalars(
                select(CustomerRepository).where(CustomerRepository.cpf == cpf)
            ).first()
            return None if row is None else CustomerDTO.model_validate(row)

    @override
    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.customer_repository import (
            CustomerRepository,
        )

        payload = _dump(customer, exclude_id="customer_id")
        with self.session_local() as session:
            row = None
            if customer.customer_id is not None:
                row = session.get(CustomerRepository, customer.customer_id)
            if row is None:
                row = CustomerRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return CustomerDTO.model_validate(row)

    @override
    def delete_customer(self, customer_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.customer_repository import (
            CustomerRepository,
        )

        with self.session_local() as session:
            row = session.get(CustomerRepository, customer_id)
            if row is not None:
                session.delete(row)
                session.commit()

    @override
    def get_person(self, cpf: str) -> PersonDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_repository import (
            PersonRepository,
        )

        with self.session_local() as session:
            row = session.get(PersonRepository, cpf)
            return None if row is None else PersonDTO.model_validate(row)

    @override
    def save_person(self, person: PersonDTO) -> PersonDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_repository import (
            PersonRepository,
        )

        payload = _dump(person)
        with self.session_local() as session:
            row = session.get(PersonRepository, person.cpf)
            if row is None:
                row = PersonRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return PersonDTO.model_validate(row)

    @override
    def delete_person(self, cpf: str) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.contacts_repository import (
            PersonContactRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_address_repository import (
            PersonAddressRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_repository import (
            PersonRepository,
        )

        with self.session_local() as session:
            for contact in session.scalars(
                select(PersonContactRepository).where(PersonContactRepository.cpf == cpf)
            ).all():
                session.delete(contact)
            for address in session.scalars(
                select(PersonAddressRepository).where(PersonAddressRepository.cpf == cpf)
            ).all():
                session.delete(address)
            row = session.get(PersonRepository, cpf)
            if row is not None:
                session.delete(row)
            session.commit()

    def _contact_payload(self, contact: PersonContactDTO) -> dict[str, Any]:
        payload = _dump(contact, exclude_id="contact_id")
        payload["contact_type"] = str(payload["contact_type"])
        return payload

    @override
    def get_contact(self, contact_id: int) -> PersonContactDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.contacts_repository import (
            PersonContactRepository,
        )

        with self.session_local() as session:
            row = session.get(PersonContactRepository, contact_id)
            return None if row is None else PersonContactDTO.model_validate(row)

    @override
    def get_contacts_by_cpf(self, cpf: str) -> list[PersonContactDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.contacts_repository import (
            PersonContactRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(PersonContactRepository).where(PersonContactRepository.cpf == cpf)
            ).all()
            return [PersonContactDTO.model_validate(row) for row in rows]

    @override
    def save_contact(self, contact: PersonContactDTO) -> PersonContactDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.contacts_repository import (
            PersonContactRepository,
        )

        payload = self._contact_payload(contact)
        with self.session_local() as session:
            row = None
            if contact.contact_id is not None:
                row = session.get(PersonContactRepository, contact.contact_id)
            if row is None:
                row = PersonContactRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return PersonContactDTO.model_validate(row)

    @override
    def delete_contact(self, contact_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.contacts_repository import (
            PersonContactRepository,
        )

        with self.session_local() as session:
            row = session.get(PersonContactRepository, contact_id)
            if row is not None:
                session.delete(row)
                session.commit()

    @override
    def get_address(self, cep_id: str) -> AddressDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.address_repository import (
            AddressRepository,
        )

        with self.session_local() as session:
            row = session.get(AddressRepository, cep_id)
            return None if row is None else AddressDTO.model_validate(row)

    @override
    def save_address(self, address: AddressDTO) -> AddressDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.address_repository import (
            AddressRepository,
        )

        payload = _dump(address)
        with self.session_local() as session:
            row = session.get(AddressRepository, address.cep_id)
            if row is None:
                row = AddressRepository(**payload)
                session.add(row)
            session.commit()
            session.refresh(row)
            return AddressDTO.model_validate(row)

    @override
    def get_person_addresses(self, cpf: str) -> list[PersonAddressDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_address_repository import (
            PersonAddressRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(PersonAddressRepository).where(PersonAddressRepository.cpf == cpf)
            ).all()
            return [PersonAddressDTO.model_validate(row) for row in rows]

    @override
    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_address_repository import (
            PersonAddressRepository,
        )

        payload = _dump(person_address, exclude_id="person_address_id")
        with self.session_local() as session:
            row = PersonAddressRepository(**payload)
            session.add(row)
            session.commit()
            session.refresh(row)
            return PersonAddressDTO.model_validate(row)

    @override
    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.address_repository import (
            AddressRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.customer_repository import (
            CustomerRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_address_repository import (
            PersonAddressRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.person_repository import (
            PersonRepository,
        )

        with self.session_local() as session:
            address_row = session.get(AddressRepository, address.cep_id)
            if address_row is None:
                session.add(AddressRepository(**_dump(address)))
                session.flush()

            person_row = session.get(PersonRepository, person.cpf)
            if person_row is None:
                session.add(PersonRepository(**_dump(person)))
                session.flush()

            session.add(
                PersonAddressRepository(
                    **_dump(person_address, exclude_id="person_address_id")
                )
            )
            customer_row = CustomerRepository(
                **_dump(customer, exclude_id="customer_id")
            )
            session.add(customer_row)
            session.commit()
            session.refresh(customer_row)
            return CustomerDTO.model_validate(customer_row)

    def _vehicle_payload(self, vehicle: VehicleDTO) -> dict[str, Any]:
        payload = _dump(vehicle, exclude_id="vehicle_id")
        payload["fuel_type"] = str(payload["fuel_type"])
        return payload

    @override
    def get_vehicle(self, vehicle_id: int) -> VehicleDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicles_repository import (
            VehicleRepository,
        )

        with self.session_local() as session:
            row = session.get(VehicleRepository, vehicle_id)
            return None if row is None else VehicleDTO.model_validate(row)

    @override
    def save_vehicle(self, vehicle: VehicleDTO) -> VehicleDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicles_repository import (
            VehicleRepository,
        )

        payload = self._vehicle_payload(vehicle)
        with self.session_local() as session:
            row = None
            if vehicle.vehicle_id is not None:
                row = session.get(VehicleRepository, vehicle.vehicle_id)
            if row is None:
                row = VehicleRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return VehicleDTO.model_validate(row)

    @override
    def delete_vehicle(self, vehicle_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicles_repository import (
            VehicleRepository,
        )

        with self.session_local() as session:
            links = session.scalars(
                select(VehicleCustomerRepository).where(
                    VehicleCustomerRepository.vehicle_id == vehicle_id
                )
            ).all()
            for link in links:
                session.delete(link)
            row = session.get(VehicleRepository, vehicle_id)
            if row is not None:
                session.delete(row)
            session.commit()

    @override
    def get_vehicle_customer_by_vehicle_id(self, vehicle_id: int) -> VehicleCustomerDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )

        with self.session_local() as session:
            row = session.scalars(
                select(VehicleCustomerRepository).where(
                    VehicleCustomerRepository.vehicle_id == vehicle_id
                )
            ).first()
            return None if row is None else VehicleCustomerDTO.model_validate(row)

    @override
    def get_vehicle_customer_by_plate(self, plate: str) -> VehicleCustomerDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )

        with self.session_local() as session:
            row = session.scalars(
                select(VehicleCustomerRepository).where(VehicleCustomerRepository.plate == plate)
            ).first()
            return None if row is None else VehicleCustomerDTO.model_validate(row)

    @override
    def get_vehicle_customers_by_customer_id(self, customer_id: int) -> list[VehicleCustomerDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(VehicleCustomerRepository).where(
                    VehicleCustomerRepository.customer_id == customer_id
                )
            ).all()
            return [VehicleCustomerDTO.model_validate(row) for row in rows]

    @override
    def save_vehicle_customer(self, vehicle_customer: VehicleCustomerDTO) -> VehicleCustomerDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )

        payload = _dump(vehicle_customer, exclude_id="vehicle_customer_id")
        with self.session_local() as session:
            row = None
            if vehicle_customer.vehicle_customer_id is not None:
                row = session.get(VehicleCustomerRepository, vehicle_customer.vehicle_customer_id)
            if row is None:
                row = VehicleCustomerRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return VehicleCustomerDTO.model_validate(row)

    @override
    def save_new_vehicle_registration(
        self,
        vehicle: VehicleDTO,
        vehicle_customer: VehicleCustomerDTO,
    ) -> VehicleDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicles_repository import (
            VehicleRepository,
        )

        with self.session_local() as session:
            vehicle_row = VehicleRepository(**self._vehicle_payload(vehicle))
            session.add(vehicle_row)
            session.flush()
            link_payload = _dump(vehicle_customer, exclude_id="vehicle_customer_id")
            link_payload["vehicle_id"] = vehicle_row.vehicle_id
            session.add(VehicleCustomerRepository(**link_payload))
            session.commit()
            session.refresh(vehicle_row)
            return VehicleDTO.model_validate(vehicle_row)

    @override
    def get_vehicle_customer(self, vehicle_customer_id: int) -> VehicleCustomerDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.vehicle_customer_repository import (
            VehicleCustomerRepository,
        )

        with self.session_local() as session:
            row = session.get(VehicleCustomerRepository, vehicle_customer_id)
            return None if row is None else VehicleCustomerDTO.model_validate(row)

    @override
    def get_user(self, user_id: int) -> UserDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.user_repository import (
            UserRepository,
        )

        with self.session_local() as session:
            row = session.get(UserRepository, user_id)
            return None if row is None else UserDTO.model_validate(row)

    @override
    def save_user(self, user: UserDTO) -> UserDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.user_repository import (
            UserRepository,
        )

        payload = _dump(user, exclude_id="user_id")
        payload["user_type"] = str(payload["user_type"])
        with self.session_local() as session:
            row = None
            if user.user_id is not None:
                row = session.get(UserRepository, user.user_id)
            if row is None:
                row = UserRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return UserDTO.model_validate(row)

    @override
    def get_service(self, service_id: int) -> ServiceDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_repository import (
            ServiceRepository,
        )

        with self.session_local() as session:
            row = session.get(ServiceRepository, service_id)
            return None if row is None else ServiceDTO.model_validate(row)

    @override
    def save_service(self, service: ServiceDTO) -> ServiceDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_repository import (
            ServiceRepository,
        )

        payload = _dump(service, exclude_id="service_id")
        with self.session_local() as session:
            row = None
            if service.service_id is not None:
                row = session.get(ServiceRepository, service.service_id)
            if row is None:
                row = ServiceRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return ServiceDTO.model_validate(row)

    @override
    def delete_service(self, service_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_repository import (
            ServiceRepository,
        )

        with self.session_local() as session:
            row = session.get(ServiceRepository, service_id)
            if row is not None:
                session.delete(row)
                session.commit()

    @override
    def get_part(self, part_id: int) -> PartDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.part_repository import (
            PartRepository,
        )

        with self.session_local() as session:
            row = session.get(PartRepository, part_id)
            return None if row is None else PartDTO.model_validate(row)

    @override
    def save_part(self, part: PartDTO) -> PartDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.part_repository import (
            PartRepository,
        )

        payload = _dump(part, exclude_id="part_id")
        with self.session_local() as session:
            row = None
            if part.part_id is not None:
                row = session.get(PartRepository, part.part_id)
            if row is None:
                row = PartRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return PartDTO.model_validate(row)

    @override
    def delete_part(self, part_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.part_repository import (
            PartRepository,
        )

        with self.session_local() as session:
            row = session.get(PartRepository, part_id)
            if row is not None:
                session.delete(row)
                session.commit()

    def _order_payload(self, order: ServiceOrderDTO) -> dict[str, Any]:
        payload = _dump(order, exclude_id="order_id")
        payload["status"] = str(payload["status"])
        return payload

    @override
    def get_service_order(self, order_id: int) -> ServiceOrderDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_order_repository import (
            ServiceOrderRepository,
        )

        with self.session_local() as session:
            row = session.get(ServiceOrderRepository, order_id)
            return None if row is None else ServiceOrderDTO.model_validate(row)

    @override
    def save_service_order(self, order: ServiceOrderDTO) -> ServiceOrderDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_order_repository import (
            ServiceOrderRepository,
        )

        payload = self._order_payload(order)
        with self.session_local() as session:
            row = None
            if order.order_id is not None:
                row = session.get(ServiceOrderRepository, order.order_id)
            if row is None:
                row = ServiceOrderRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return ServiceOrderDTO.model_validate(row)

    @override
    def delete_service_order(self, order_id: int) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_part_repository import (
            OrderPartRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_service_repository import (
            OrderServiceRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_order_repository import (
            ServiceOrderRepository,
        )

        with self.session_local() as session:
            for model in (OrderServiceRepository, OrderPartRepository):
                for line in session.scalars(
                    select(model).where(model.order_id == order_id)
                ).all():
                    session.delete(line)
            row = session.get(ServiceOrderRepository, order_id)
            if row is not None:
                session.delete(row)
            session.commit()

    @override
    def get_order_service_lines(self, order_id: int) -> list[OrderServiceLineDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_service_repository import (
            OrderServiceRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(OrderServiceRepository).where(OrderServiceRepository.order_id == order_id)
            ).all()
            return [OrderServiceLineDTO.model_validate(row) for row in rows]

    @override
    def get_order_part_lines(self, order_id: int) -> list[OrderPartLineDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_part_repository import (
            OrderPartRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(OrderPartRepository).where(OrderPartRepository.order_id == order_id)
            ).all()
            return [OrderPartLineDTO.model_validate(row) for row in rows]

    @override
    def save_order_service_line(self, line: OrderServiceLineDTO) -> OrderServiceLineDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_service_repository import (
            OrderServiceRepository,
        )

        payload = _dump(line, exclude_id="order_service_id")
        with self.session_local() as session:
            row = None
            if line.order_service_id is not None:
                row = session.get(OrderServiceRepository, line.order_service_id)
            if row is None:
                row = OrderServiceRepository(**payload)
                session.add(row)
            else:
                for key, value in payload.items():
                    setattr(row, key, value)
            session.commit()
            session.refresh(row)
            return OrderServiceLineDTO.model_validate(row)

    @override
    def save_new_service_order(
        self,
        order: ServiceOrderDTO,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> ServiceOrderDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_part_repository import (
            OrderPartRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_service_repository import (
            OrderServiceRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.service_order_repository import (
            ServiceOrderRepository,
        )

        with self.session_local() as session:
            order_row = ServiceOrderRepository(**self._order_payload(order))
            session.add(order_row)
            session.flush()
            for line in service_lines:
                payload = _dump(line, exclude_id="order_service_id")
                payload["order_id"] = order_row.order_id
                session.add(OrderServiceRepository(**payload))
            for line in part_lines:
                payload = _dump(line, exclude_id="order_part_id")
                payload["order_id"] = order_row.order_id
                session.add(OrderPartRepository(**payload))
            session.commit()
            session.refresh(order_row)
            return ServiceOrderDTO.model_validate(order_row)

    @override
    def replace_order_lines(
        self,
        order_id: int,
        service_lines: list[OrderServiceLineDTO],
        part_lines: list[OrderPartLineDTO],
    ) -> None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_part_repository import (
            OrderPartRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_service_repository import (
            OrderServiceRepository,
        )

        with self.session_local() as session:
            for model in (OrderServiceRepository, OrderPartRepository):
                for line in session.scalars(
                    select(model).where(model.order_id == order_id)
                ).all():
                    session.delete(line)
            session.flush()
            for line in service_lines:
                payload = _dump(line, exclude_id="order_service_id")
                payload["order_id"] = order_id
                session.add(OrderServiceRepository(**payload))
            for line in part_lines:
                payload = _dump(line, exclude_id="order_part_id")
                payload["order_id"] = order_id
                session.add(OrderPartRepository(**payload))
            session.commit()


    @override
    def get_order_part_line(self, order_part_id: int) -> OrderPartLineDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.order_part_repository import (
            OrderPartRepository,
        )

        with self.session_local() as session:
            row = session.get(OrderPartRepository, order_part_id)
            return None if row is None else OrderPartLineDTO.model_validate(row)

    def _stock_operation_payload(self, operation: StockOperationDTO) -> dict[str, Any]:
        payload = _dump(operation, exclude_id="operation_id")
        payload["operation_type"] = str(payload["operation_type"])
        return payload

    @override
    def get_stock_operations_by_part_id(self, part_id: int) -> list[StockOperationDTO]:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.stock_operation_repository import (
            StockOperationRepository,
        )

        with self.session_local() as session:
            rows = session.scalars(
                select(StockOperationRepository)
                .where(StockOperationRepository.part_id == part_id)
                .order_by(StockOperationRepository.operation_date)
            ).all()
            return [StockOperationDTO.model_validate(row) for row in rows]

    @override
    def get_stock_operation_by_order_part_id(
        self,
        order_part_id: int,
    ) -> StockOperationDTO | None:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.stock_operation_repository import (
            StockOperationRepository,
        )

        with self.session_local() as session:
            row = session.scalars(
                select(StockOperationRepository).where(
                    StockOperationRepository.order_part_id == order_part_id
                )
            ).first()
            return None if row is None else StockOperationDTO.model_validate(row)

    @override
    def apply_stock_operation(
        self,
        operation: StockOperationDTO,
        updated_part: PartDTO,
    ) -> StockOperationDTO:
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.part_repository import (
            PartRepository,
        )
        from src.adapters.driving.for_storing_data.rdbms_adapter.models.stock_operation_repository import (
            StockOperationRepository,
        )

        part_payload = _dump(updated_part, exclude_id="part_id")
        with self.session_local() as session:
            part_row = session.get(PartRepository, updated_part.part_id)
            if part_row is None:
                raise ValueError("Part not found")
            for key, value in part_payload.items():
                setattr(part_row, key, value)
            operation_row = StockOperationRepository(**self._stock_operation_payload(operation))
            session.add(operation_row)
            session.commit()
            session.refresh(operation_row)
            return StockOperationDTO.model_validate(operation_row)


rdbms_adapter = RdbmsAdapter()
