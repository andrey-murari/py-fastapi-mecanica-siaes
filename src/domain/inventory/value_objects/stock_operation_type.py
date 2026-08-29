from enum import StrEnum


class StockOperationType(StrEnum):
    INITIAL = "Entrada inicial"
    INBOUND = "Entrada"
    OUTBOUND = "Baixa"
