from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.domain.customers_and_services.relationship.entities import Customer
from src.infrastructure.repository.database import Base


class CustomerRepository(Base):
    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    people_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime)

    def __init__(self, customer: Customer):
        self.customer_id = customer.customer_id
        self.people_if = customer.people.person_id
        self.flag_active = customer.flag_active
        self.insertion_date = customer.insertion_date
        self.modification_date = customer.modification_date


class PeopleRepository(Base):
    __tablename__ = "people"

    cpf: Mapped[str] = mapped_column(String(11), primary_key=True)
    complete_name: Mapped[str] = mapped_column(String(255))
    cep_id: Mapped[int]
    user_id: Mapped[int]
    user_modification_id: Mapped[int]
    flag_active: Mapped[bool]
    insertion_date: Mapped[datetime]
    modification_date: Mapped[datetime]

# class CustomerModel(Base):
#     __tablename__ = "customers"

#     customer_id: Mapped[int] = mapped_column(primary_key=True)
#     cpf: Mapped[str] = mapped_column(ForeignKey("people.cpf"))
#     flag_active: Mapped[bool]
#     insertion_date: Mapped[datetime]
#     modification_date: Mapped[datetime]
#     people: Mapped[PeopleModel] = relationship()


# class SqlCustomerRepository:
#     def __init__(self, session: Session) -> None:
#         self._session = session

#     def get_by_id(self, customer_id: int) -> Customer | None:
#         row = self._session.get(CustomerModel, customer_id)
#         if row is None:
#             return None
#         return Customer(
#             customer_id=row.customer_id,
#             people=People.model_validate(row.people, from_attributes=True),
#             flag_active=row.flag_active,
#             insertion_date=row.insertion_date,
#             modification_date=row.modification_date,
#         )

#     def save(self, customer: Customer | dict) -> Customer:
#         customer = Customer.model_validate(customer)
#         if self._session.get(PeopleModel, customer.people.cpf) is None:
#             self._session.add(PeopleModel(**customer.people.model_dump()))
#         self._session.add(
#             CustomerModel(
#                 customer_id=customer.customer_id,
#                 cpf=customer.people.cpf,
#                 flag_active=customer.flag_active,
#                 insertion_date=customer.insertion_date,
#                 modification_date=customer.modification_date,
#             )
#         )
#         self._session.commit()
#         return customer
