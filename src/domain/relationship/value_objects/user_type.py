from enum import StrEnum

class UserType(StrEnum):
    ADMIN = "Administrador"
    USER = "Usuário"
    VISITOR = "Visitante"
    CLIENT = "Cliente"