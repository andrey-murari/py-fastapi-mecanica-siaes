from datetime import datetime

from pydantic import BaseModel


class Mecanico(BaseModel):
    mecanico_id: int | None = None
    cpf: str
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
