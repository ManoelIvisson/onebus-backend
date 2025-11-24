from models.coordenada_viagem import CoordenadaViagem
from models.motorista_veiculo import motorista_veiculo
from config import db
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Integer, String

if TYPE_CHECKING:
  from models.motorista import Motorista
  from models.viagem import Viagem

class Veiculo(db.Model):
  __tablename__ = 'veiculo'

  id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
  placa: Mapped[str] = mapped_column(String(7), unique=True)
  tipo: Mapped[str] = mapped_column(String(20))
  modelo: Mapped[str] = mapped_column(String(30))
  mac_embarcado: Mapped[str] = mapped_column(String(16))

  motoristas: Mapped[list['Motorista']] = relationship(
    secondary=motorista_veiculo, back_populates="veiculos"
  )

  viagem: Mapped[list['Viagem']] = relationship()
  
  def get_coordenada_atual(self):
    coord = CoordenadaViagem.query \
      .filter_by(mac=self.mac_embarcado) \
      .order_by(CoordenadaViagem.criado_em.desc()) \
      .first()
      
    if not coord:
      return None
    
    return {
      "latitude": coord.latitude,
      "longitude": coord.longitude,
      "criado_em": coord.criado_em.isoformat(),
    }

  def to_dict(self):
    return {
      "id": self.id,
      "tipo": self.tipo,
      "placa": self.placa,
      "modelo": self.modelo,
      "mac_embarcado": self.mac_embarcado,
      "coordenada_atual": self.get_coordenada_atual()
    }
