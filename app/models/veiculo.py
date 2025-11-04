from models.motorista_veiculo import motorista_veiculo
from config import db
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Integer, String

if TYPE_CHECKING:
  from models.motorista import Motorista
  from app.models.rastreador import Rastreador
  from models.trajeto import Trajeto

class Veiculo(db.Model):
  __tablename__ = 'veiculo'

  id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
  placa: Mapped[str] = mapped_column(String(7), unique=True)
  tipo: Mapped[str] = mapped_column(String(20))

  motoristas: Mapped[list['Motorista']] = relationship(
    secondary=motorista_veiculo, back_populates="veiculos"
  )
  rastreador_id: Mapped[int] = mapped_column(Integer, ForeignKey("rastreador.id"), unique=True)
  
  rastreador: Mapped['Rastreador'] = relationship("Rastreador", back_populates="veiculo")

  # relacionamento N trajetos de viagem para 1 carro
  # cada carro pode ter vários trajetos associados
  # ao ser cadastrado um novo trajeto nesse campo, ele se comunica com a coluna estrangeira da tabela trajeto
  trajeto: Mapped[list['Trajeto']] = relationship()

  def to_dict(self):
    return {
      "id": self.id,
      "tipo": self.tipo,
      "placa": self.placa
    }
