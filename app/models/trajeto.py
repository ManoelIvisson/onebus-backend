from config import db
from typing import TYPE_CHECKING
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
  from models.veiculo import Veiculo
  from models.ponto_trajeto import PontoTrajeto

class Trajeto(db.Model):
  __tablename__ = 'trajeto'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(50))
  horario_inicio: Mapped[datetime.time] = mapped_column()
  horario_final: Mapped[datetime.time] = mapped_column()
  trajeto_planejado: Mapped[bool] = mapped_column(default=False)
  
  # coluna de chave estrangeira
  veiculo_id: Mapped[int] = mapped_column(ForeignKey('veiculo.id'), nullable=True)

  # relacionamento para acesso na via contrária
  # se comunica com o relacionamento com Veiculo trajeto
  # relacionamento 1 veiculo para N trajetos
  # cada trajeto tem apenas 1 carro
  veiculo: Mapped['Veiculo'] = relationship(back_populates='trajeto')

  # relacionamento N pontos de trajeto para 1 trajeto
  # cada trajeto pode ter vários pontos associados
  # ao ser cadastrado um novo ponto de trajeto nesse campo, ele se comunica com a coluna estrangeira da tabela trajeto
  pontos: Mapped[list['PontoTrajeto']] = relationship()