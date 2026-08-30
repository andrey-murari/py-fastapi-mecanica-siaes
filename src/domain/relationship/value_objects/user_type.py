from enum import StrEnum

class UserType(StrEnum):
    ADMIN = "Administrador"
    USER = "Usuário"
    VISITOR = "Visitante"
    CLIENT = "Cliente"
    MECHANIC = "Mecânico"
    ATTENDANT = "Atendente"
    STOCKIST = "Estoquista"
    BUYER = "Comprador"
