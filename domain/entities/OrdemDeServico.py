from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrdemDeServico(BaseModel):
    ordem_de_servico_id: int | None = None
    cliente_id: int
    veiculo_cliente_id: int
    quilometragem: int | None = None
    valor_total: Decimal = Decimal("0")
    valor_total_pecas: Decimal = Decimal("0")
    valor_total_servicos: Decimal = Decimal("0")
    data_solicitacao: datetime | None = None
    data_inicio: datetime | None = None
    data_fim: datetime | None = None
    tipo_status_id: int
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
