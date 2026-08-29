from abc import ABC, abstractmethod

from src.ports.driver.for_manage_inventory.dto.inventory_dto import (
    InventoryDetailDTO,
    InventoryQuantityDTO,
    StockOperationCreateDTO,
    StockOperationResultDTO,
)


class ForManageInventory(ABC):
    @abstractmethod
    def apply_operation(self, operation: StockOperationCreateDTO) -> StockOperationResultDTO:
        pass

    @abstractmethod
    def read_inventory(self, part_id: int) -> InventoryDetailDTO:
        pass

    @abstractmethod
    def read_quantity(self, part_id: int) -> InventoryQuantityDTO:
        pass
