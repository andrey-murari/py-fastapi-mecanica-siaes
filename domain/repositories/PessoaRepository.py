
from typing import Optional
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class Pessoa(Base):
    __tablename__ = "pessoa"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    sobrenome: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    data_nascimento: Mapped[date]
    def __repr__(self) -> str:
        return f"Pessoa(id={self.id!r}, name={self.nome!r}, fullname={self.sobrenome!r})"