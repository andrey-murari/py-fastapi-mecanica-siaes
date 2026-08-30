from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.domain.inventory.value_objects.stock_operation_type import StockOperationType


class StockOperation(BaseModel):
    """A ledger entry that changes Part.available_quantity."""

    model_config = ConfigDict(from_attributes=True)

    operation_id: int | None = None
    part_id: int = Field(gt=0)
    operation_type: StockOperationType
    quantity: int = Field(gt=0)
    order_part_id: int | None = Field(default=None, gt=0)
    operation_date: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def validate_order_part_link(self) -> "StockOperation":
        if self.operation_type is StockOperationType.OUTBOUND:
            if self.order_part_id is None:
                raise ValueError("OUTBOUND requires order_part_id")
        elif self.order_part_id is not None:
            raise ValueError("order_part_id is only allowed for OUTBOUND")
        return self
