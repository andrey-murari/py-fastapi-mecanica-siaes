from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PecaInsumo(BaseModel):
    peca_insumo_id: int | None = None
    descricao: str
    marca: str | None = None
    fabricante: str | None = None
    valor_unitario: Decimal
    quantidade_disponivel: int = 0
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
