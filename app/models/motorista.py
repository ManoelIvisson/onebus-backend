from app.config import db
from typing import TYPE_CHECKING, Optional
from models.usuario import Usuario
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey

if TYPE_CHECKING:
    from models.veiculo import Veiculo
class Motorista(db.Model, Usuario):
    __tablename__ = 'motorista'

    cnh: Mapped[int] = mapped_column(Integer, unique=True)
    veiculo: Mapped[Optional[int]] = mapped_column(ForeignKey('veiculo.id'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Veiculo motorista_cnh
    # relacionamento 1 veiculo para N motoristas
    # cada motorista tem apenas 1 veiculo
    veiculo: Mapped['Veiculo'] = relationship(back_populates='id')