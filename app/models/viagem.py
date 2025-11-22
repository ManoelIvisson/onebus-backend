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
  horario_final: Mapped[datetime.time] = mapped_column()
  atrasou: Mapped[bool] = mapped_column(default=False)
  desviou: Mapped[bool] = mapped_column(default=False)
  status: Mapped[str] = mapped_column(String(15), default='ativa')
  
  veiculo_id: Mapped[int] = mapped_column(ForeignKey('veiculo.id'), nullable=True)
  veiculo: Mapped['Veiculo'] = relationship(back_populates='viagem')

  coordenadas: Mapped[list['CoordenadaViagem']] = relationship()