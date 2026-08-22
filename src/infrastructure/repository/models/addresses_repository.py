from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.customers_and_services.relationship.entities import Address
from src.infrastructure.repository.database import Base


class AddressRepository(Base):
    __tablename__ = "address"

    cep_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    street: Mapped[str] = mapped_column(String(255))
    neighborhood: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(2))
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, address: Address):
        super().__init__(
            cep_id=address.cep_id,
            street=address.street,
            neighborhood=address.neighborhood,
            city=address.city,
            state=address.state,
            user_modification_id=address.user_modification_id,
            flag_active=address.flag_active,
            insertion_date=address.insertion_date,
            modification_date=address.modification_date,
        )
