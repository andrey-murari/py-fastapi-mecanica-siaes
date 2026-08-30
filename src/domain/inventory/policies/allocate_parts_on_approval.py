from src.domain.order_services.entities.order_services import ServiceOrder
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import ForManageInventory
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import ServiceOrderDTO
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class AllocatePartsOnApproval:
    """DDD policy: runs by itself after the client approves the quote.

    Checks live stock for each order part and sends the OS to separating
    or purchasing.
    """

    def __init__(self, storage: ForStoringData, inventory: ForManageInventory) -> None:
        self._storage = storage
        self._inventory = inventory

    def apply(self, order: ServiceOrderDTO) -> ServiceOrderDTO:
        if order.order_id is None or order.status is not OrderStatus.APPROVED:
            return order

        available = True
        for line in self._storage.get_order_part_lines(order.order_id):
            stock = self._inventory.read_quantity(line.part_id)
            if stock.available_quantity < line.quantity:
                available = False
                break

        next_status = (
            OrderStatus.PARTS_SEPARATING if available else OrderStatus.PARTS_PURCHASING
        )
        updated = ServiceOrder.model_validate(order).with_status(next_status)
        return self._storage.save_service_order(ServiceOrderDTO.model_validate(updated))
