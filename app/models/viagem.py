from config import db
from typing import TYPE_CHECKING
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
  from models.veiculo import Veiculo
  from models.coordenada_viagem import CoordenadaViagem

class Viagem(db.Model):
  __tablename__ = 'viagem'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  horario_inicio: Mapped[datetime.time] = mapped_column()
  horario_final: Mapped[datetime.time] = mapped_column(nullable=True)
  atrasou: Mapped[bool] = mapped_column(default=False)
  desviou: Mapped[bool] = mapped_column(default=False)
  status: Mapped[str] = mapped_column(String(15), default='ativa')
  
  veiculo_id: Mapped[int] = mapped_column(ForeignKey('veiculo.id'), nullable=True)
  veiculo: Mapped['Veiculo'] = relationship(back_populates='viagem')

  coordenadas: Mapped[list['CoordenadaViagem']] = relationship()
  
  def to_dict(self, incluir_coordenadas):
    data = {
      "id": self.id,
      "horario_inicio": self.horario_inicio.strftime("%H:%M") if self.horario_inicio else None,
      "horario_final": self.horario_final.strftime("%H:%M") if self.horario_final else None,
      "atrasou": self.atrasou,
      "desviou": self.desviou,
      "status": self.status
    }
    
    if incluir_coordenadas:
      data["coordenadas"] = [c.to_dict() for c in self.coordenadas]
    
    return data