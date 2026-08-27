from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class VehicleCustomerRepository(Base):
    __tablename__ = "vehicle_customer"

    vehicle_customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey("vehicle.vehicle_id"))
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customer.customer_id"))
    plate: Mapped[str] = mapped_column(String(7), unique=True)
    color: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
