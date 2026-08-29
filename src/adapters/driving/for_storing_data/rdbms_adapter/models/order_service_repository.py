from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class OrderServiceRepository(Base):
    __tablename__ = "order_service"

    order_service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_order.order_id"))
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("service.service_id"))
    mechanic_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("user.user_id"), nullable=True
    )
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
