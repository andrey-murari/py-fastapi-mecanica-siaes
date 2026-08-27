from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    SHIPPED = "Em execução"
    DELIVERED = "Encerrado"
    CANCELLED = "Cancelado"