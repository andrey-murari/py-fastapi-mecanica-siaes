from datetime import datetime

from pydantic import BaseModel


class TipoCombustivel(BaseModel):
    tipo_combustivel_id: int | None = None
    tipo: str
    descricao: str | None = None
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
