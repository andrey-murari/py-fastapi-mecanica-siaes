from domain.entities.Cliente import Cliente


class ConsultarCliente:
    """Consulta se um cliente já possui cadastro no sistema a partir do CPF."""

    def __init__(self, clientes: list[Cliente] | None = None):
        self._clientes = list(clientes or [])

    def executar_consulta(self, cpf: str) -> str:
        encontrado = any(cliente.cpf == cpf for cliente in self._clientes)
        if encontrado:
            return "o cliente já possui cadastro"
        return "o cliente não possui cadastro"
