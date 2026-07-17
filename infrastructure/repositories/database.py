from sqlalchemy.orm import Session

from domain.entities.Cliente import Cliente
from infrastructure.repositories.engine import engine

cliente = {
        'nome': 'spongebob',
        'sobrenome': 'Spongebob Squarepants',
        'email': 'spongebob@outlook.com',
        'data_nascimento': '2000-01-01'
}

with Session(engine) as session:
    spongebob = Cliente(**cliente)

    session.add_all([spongebob])

    session.commit()