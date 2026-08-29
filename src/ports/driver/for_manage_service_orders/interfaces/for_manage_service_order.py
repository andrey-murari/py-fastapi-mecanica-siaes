from abc import ABC, abstractmethod

from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderStatusUpdateDTO,
    ServiceOrderCreateDTO,
    ServiceOrderDetailDTO,
    ServiceOrderUpdateDTO,
)


class ForManageServiceOrder(ABC):
    @abstractmethod
    def create_service_order(self, order: ServiceOrderCreateDTO) -> ServiceOrderDetailDTO:
        pass

    @abstractmethod
    def read_service_order(self, order_id: int) -> ServiceOrderDetailDTO:
        pass

    @abstractmethod
    def update_service_order(
        self,
        order_id: int,
        order: ServiceOrderUpdateDTO,
    ) -> ServiceOrderDetailDTO:
        pass

    @abstractmethod
    def delete_service_order(self, order_id: int) -> dict:
        pass

    @abstractmethod
    def assign_mechanic(self, order_id: int, mechanic: AssignMechanicDTO) -> ServiceOrderDetailDTO:
        pass

    @abstractmethod
    def change_status(self, order_id: int, status: OrderStatusUpdateDTO) -> ServiceOrderDetailDTO:
        pass
