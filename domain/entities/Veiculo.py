from datetime import datetime

from pydantic import BaseModel


class Veiculo(BaseModel):
    veiculo_id: int | None = None
    modelo: str
    marca: str
    ano_fabricacao: str
    ano_modelo: str
    motorizacao: str | None = None
    tipo_combustivel_id: int
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
