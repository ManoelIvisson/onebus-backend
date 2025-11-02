from config import db
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from datetime import datetime

if TYPE_CHECKING:
  from models.trajeto import Trajeto
  from models.cidadao import Cidadao

class PontoTrajeto(db.Model):
  __tablename__ = 'ponto_trajeto'

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  latitude: Mapped[str] = mapped_column(String)
  longitude: Mapped[str] = mapped_column(String)
  criado_em: Mapped[datetime] = mapped_column()

  # coluna de chave estrangeira
  trajeto_id: Mapped[int] = mapped_column(ForeignKey('trajeto.id'))

  # relacionamento para acesso na via contrária
  # se comunica com o relacionamento com Trajeto trajeto_ponto
  # relacionamento 1 trajeto para N pontos
  # cada ponto tem apenas 1 trajeto
  trajeto: Mapped['Trajeto'] = relationship(back_populates='trajeto_ponto')