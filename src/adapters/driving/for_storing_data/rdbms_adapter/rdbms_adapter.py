from typing import Any, override
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerDTO,
    PersonAddressDTO,
    PersonDTO,
)
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
            customer_repository,
            person_address_repository,
            person_repository,
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


rdbms_adapter = RdbmsAdapter()
