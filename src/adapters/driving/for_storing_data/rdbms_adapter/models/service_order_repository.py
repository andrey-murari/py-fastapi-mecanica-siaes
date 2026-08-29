from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class ServiceOrderRepository(Base):
    __tablename__ = "service_order"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customer.customer_id"))
    vehicle_customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vehicle_customer.vehicle_customer_id")
    )
    mileage: Mapped[int] = mapped_column(Integer)
    services_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    parts_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(30))
    request_date: Mapped[datetime] = mapped_column(DateTime)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
