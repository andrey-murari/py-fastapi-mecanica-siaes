from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from src.domain.customers_and_services.relationship.entities.customers import (
    Customer,
)
from src.domain.customers_and_services.relationship.entities.people import People


class Base(DeclarativeBase):
    pass


class PeopleModel(Base):
    __tablename__ = "people"

    cpf: Mapped[str] = mapped_column(String(11), primary_key=True)
    complete_name: Mapped[str] = mapped_column(String(255))
    cep_id: Mapped[int]
    user_id: Mapped[int]
    user_modification_id: Mapped[int]
    flag_active: Mapped[bool]
    insertion_date: Mapped[datetime]
    modification_date: Mapped[datetime]


class CustomerModel(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    cpf: Mapped[str] = mapped_column(ForeignKey("people.cpf"))
    flag_active: Mapped[bool]
    insertion_date: Mapped[datetime]
    modification_date: Mapped[datetime]
    people: Mapped[PeopleModel] = relationship()


# session.add(PeopleModel(cpf="12345678901", complete_name="John Doe", cep_id=1, user_id=1, user_modification_id=1, flag_active=True, insertion_date=datetime.now(), modification_date=datetime.now()))
# session.add(CustomerModel(customer_id=1, cpf="12345678901", flag_active=True, insertion_date=datetime.now(), modification_date=datetime.now()))
# session.commit()

class SqlCustomerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session
        Base.metadata.create_all(session.bind)

    def get_by_id(self, customer_id: int) -> Customer | None:
        row = self._session.get(CustomerModel, customer_id)
        if row is None:
            return None
        return Customer(
            customer_id=row.customer_id,
            people=People.model_validate(row.people, from_attributes=True),
            flag_active=row.flag_active,
            insertion_date=row.insertion_date,
            modification_date=row.modification_date,
        )
