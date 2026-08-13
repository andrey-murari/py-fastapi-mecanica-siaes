from datetime import datetime

from pydantic import BaseModel


class OrdemDeServicoServico(BaseModel):
    ordem_de_servico_servico_id: int | None = None
    ordem_de_servico_id: int
    servico_id: int
    mecanico_id: int
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
