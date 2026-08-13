from datetime import datetime

from pydantic import BaseModel


class VeiculoCliente(BaseModel):
    veiculo_cliente_id: int | None = None
    veiculo_id: int
    cliente_id: int
    placa: str
    cor: str | None = None
    descricao_veiculo: str | None = None
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_atualizacao: datetime | None = None
