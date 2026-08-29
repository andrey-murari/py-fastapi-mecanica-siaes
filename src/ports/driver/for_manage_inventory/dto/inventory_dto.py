from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.domain.inventory.value_objects.stock_operation_type import StockOperationType


class StockOperationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation_id: int | None = None
    part_id: int
    operation_type: StockOperationType
    quantity: int
    order_part_id: int | None = None
    operation_date: datetime = Field(default_factory=datetime.now)


class StockOperationCreateDTO(BaseModel):
    part_id: int = Field(examples=[1])
    operation_type: StockOperationType
    quantity: int = Field(gt=0, examples=[10])
    order_part_id: int | None = Field(default=None, examples=[1])


class StockOperationResultDTO(StockOperationDTO):
    available_quantity: int


class InventoryDetailDTO(BaseModel):
    part_id: int
    available_quantity: int
    operations: list[StockOperationDTO] = Field(default_factory=list)


class InventoryQuantityDTO(BaseModel):
    available_quantity: int
