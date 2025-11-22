from config import db
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from datetime import datetime

if TYPE_CHECKING:
  from models.viagem import Viagem

class CoordenadaViagem(db.Model):
  __tablename__ = 'coordenada_viagem'

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  latitude: Mapped[str] = mapped_column(String)
  longitude: Mapped[str] = mapped_column(String)
  criado_em: Mapped[datetime] = mapped_column()
  mac: Mapped[str] = mapped_column(String, nullable=True)
  
  viagem_id: Mapped[int] = mapped_column(ForeignKey('viagem.id'), nullable=True)
  viagem: Mapped['Viagem'] = relationship(back_populates='coordenadas')