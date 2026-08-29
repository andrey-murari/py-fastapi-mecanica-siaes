from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.driving.for_storing_data.rdbms_adapter.rdbms_adapter import Base


class StockOperationRepository(Base):
    __tablename__ = "stock_operation"

    operation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(Integer, ForeignKey("part.part_id"))
    operation_type: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer)
    order_part_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("order_part.order_part_id"), unique=True, nullable=True
    )
    operation_date: Mapped[datetime] = mapped_column(DateTime)
