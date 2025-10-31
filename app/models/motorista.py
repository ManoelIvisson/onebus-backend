from models.motorista_veiculo import motorista_veiculo
from config import db
from typing import TYPE_CHECKING, Optional
from models.usuario import Usuario
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, String

if TYPE_CHECKING:
    from models.veiculo import Veiculo
class Motorista(Usuario):
    __tablename__ = 'motorista'

    cnh: Mapped[str] = mapped_column(String, unique=True)
    veiculos: Mapped[list['Veiculo']] = relationship(
        secondary=motorista_veiculo, back_populates="motoristas"
    )
