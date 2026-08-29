from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class PersonContactRepository(Base):
    __tablename__ = "person_contact"

    contact_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cpf: Mapped[str] = mapped_column(String(11), ForeignKey("person.cpf"))
    contact_type: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(255))
    flag_preferred: Mapped[bool] = mapped_column(Boolean)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
