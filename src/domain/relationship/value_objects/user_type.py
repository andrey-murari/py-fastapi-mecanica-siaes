from enum import Enum

class UserType(Enum):
    ADMIN = "Administrador"
    USER = "Usuário"
    VISITOR = "Visitante"
    CLIENT = "Cliente"