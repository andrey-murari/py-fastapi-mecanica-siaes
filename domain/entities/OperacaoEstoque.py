from datetime import datetime

from pydantic import BaseModel


class OperacaoEstoque(BaseModel):
    operacao_estoque_id: int | None = None
    ordem_de_servico_pecas_insumos_id: int | None = None
    peca_insumo_id: int
    tipo_operacao_estoque_id: int
    quantidade: int
    data_operacao: datetime | None = None
