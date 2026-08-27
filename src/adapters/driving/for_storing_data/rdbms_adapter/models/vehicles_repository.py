from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class VehicleRepository(Base):
    __tablename__ = "vehicle"

    vehicle_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(100))
    brand: Mapped[str] = mapped_column(String(50))
    manufacture_year: Mapped[str] = mapped_column(String(4))
    model_year: Mapped[str] = mapped_column(String(4))
    engine: Mapped[str] = mapped_column(String(50))
    fuel_type: Mapped[str] = mapped_column(String(20))
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
