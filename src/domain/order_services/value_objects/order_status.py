from enum import StrEnum


class OrderStatus(StrEnum):
    WAITING_MECHANIC = "Aguardando mecânico"
    WAITING_DIAGNOSIS = "Aguardando diagnóstico"
    WAITING_APPROVAL = "Aguardando aprovação"
    IN_PROGRESS = "Em execução"
    FINISHED = "Finalizada"
    DELIVERED = "Entregue"
    CANCELLED = "Cancelada"


ALLOWED_TRANSITIONS: dict[OrderStatus, tuple[OrderStatus, ...]] = {
    OrderStatus.WAITING_MECHANIC: (OrderStatus.WAITING_DIAGNOSIS, OrderStatus.CANCELLED),
    OrderStatus.WAITING_DIAGNOSIS: (OrderStatus.WAITING_APPROVAL, OrderStatus.CANCELLED),
    OrderStatus.WAITING_APPROVAL: (OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED),
    OrderStatus.IN_PROGRESS: (OrderStatus.FINISHED, OrderStatus.CANCELLED),
    OrderStatus.FINISHED: (OrderStatus.DELIVERED,),
    OrderStatus.DELIVERED: (),
    OrderStatus.CANCELLED: (),
}
