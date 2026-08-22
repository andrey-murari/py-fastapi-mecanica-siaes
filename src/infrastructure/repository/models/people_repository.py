from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.customers_and_services.relationship.entities import People
from src.infrastructure.repository.database import Base


class PeopleRepository(Base):
    __tablename__ = "people"

    cpf: Mapped[str] = mapped_column(String(11), primary_key=True)
    complete_name: Mapped[str] = mapped_column(String(255))
    cep_id: Mapped[str] = mapped_column(String(8))
    user_id: Mapped[int] = mapped_column(Integer)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, people: People):
        super().__init__(
            cpf=people.cpf,
            complete_name=people.complete_name,
            cep_id=str(people.cep_id),
            user_id=people.user_id,
            user_modification_id=people.user_modification_id,
            flag_active=people.flag_active,
            insertion_date=people.insertion_date,
            modification_date=people.modification_date,
        )