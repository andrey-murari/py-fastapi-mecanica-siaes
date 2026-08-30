from enum import StrEnum


class OrderStatus(StrEnum):
    WAITING_MECHANIC = "Aguardando mecânico"
    WAITING_DIAGNOSIS = "Aguardando diagnóstico"
    DIAGNOSIS_COMPLETED = "Diagnóstico concluído"
    WAITING_APPROVAL = "Aguardando aprovação"
    APPROVED = "Aprovada"
    PARTS_SEPARATING = "Peças em separação no estoque"
    PARTS_PURCHASING = "Em processo de compra das peças/insumos"
    READY_TO_START = "Pronto para iniciar"
    IN_PROGRESS = "Em execução"
    FINISHED = "Finalizada"
    DELIVERED = "Entregue"
    REJECTED = "Rejeitada"
    CANCELLED = "Cancelada"


ALLOWED_TRANSITIONS: dict[OrderStatus, tuple[OrderStatus, ...]] = {
    OrderStatus.WAITING_MECHANIC: (OrderStatus.WAITING_DIAGNOSIS, OrderStatus.CANCELLED),
    OrderStatus.WAITING_DIAGNOSIS: (OrderStatus.DIAGNOSIS_COMPLETED, OrderStatus.CANCELLED),
    OrderStatus.DIAGNOSIS_COMPLETED: (OrderStatus.WAITING_APPROVAL, OrderStatus.CANCELLED),
    OrderStatus.WAITING_APPROVAL: (OrderStatus.APPROVED, OrderStatus.REJECTED, OrderStatus.CANCELLED),
    OrderStatus.APPROVED: (
        OrderStatus.PARTS_SEPARATING,
        OrderStatus.PARTS_PURCHASING,
        OrderStatus.CANCELLED,
    ),
    OrderStatus.PARTS_SEPARATING: (OrderStatus.READY_TO_START, OrderStatus.CANCELLED),
    OrderStatus.PARTS_PURCHASING: (
        OrderStatus.PARTS_SEPARATING,
        OrderStatus.READY_TO_START,
        OrderStatus.CANCELLED,
    ),
    OrderStatus.READY_TO_START: (OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED),
    OrderStatus.IN_PROGRESS: (OrderStatus.FINISHED, OrderStatus.CANCELLED),
    OrderStatus.FINISHED: (OrderStatus.DELIVERED,),
    OrderStatus.DELIVERED: (),
    OrderStatus.REJECTED: (),
    OrderStatus.CANCELLED: (),
}
