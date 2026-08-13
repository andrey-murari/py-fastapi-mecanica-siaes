from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Servico(BaseModel):
    servico_id: int | None = None
    descricao: str
    valor_servico: Decimal
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
