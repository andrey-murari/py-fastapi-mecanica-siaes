from datetime import datetime

from pydantic import BaseModel


class Usuario(BaseModel):
    usuario_id: int | None = None
    tipo_usuario_id: int
    login: str
    senha: str
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
