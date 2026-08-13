from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrdemDeServicoPecaInsumo(BaseModel):
    ordem_de_servico_id: int
    peca_insumo_id: int
    quantidade: int
    valor_total: Decimal
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
