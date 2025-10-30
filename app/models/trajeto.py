from app.config import db
from typing import TYPE_CHECKING
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

if TYPE_CHECKING:
    from models.veiculo import Veiculo
    from models.ponto_trajeto import PontoTrajeto

class Trajeto(db.Model):
    __tablename__ = 'trajeto'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    servico_prestado: Mapped[str] = mapped_column(String(50))
    ponto_origem: Mapped[str] = mapped_column(String(50))
    ponto_destino: Mapped[str] = mapped_column(String(50))
    horario_estimado: Mapped[datetime.time] = mapped_column()
    
    # coluna de chave estrangeira
    carro_placa: Mapped[str] = mapped_column(ForeignKey('carro.placa'))

    # relacionamento para acesso na via contrária
    # se comunica com o relacionamento com Veiculo trajeto
    # relacionamento 1 veiculo para N trajetos
    # cada trajeto tem apenas 1 carro
    carro: Mapped['Veiculo'] = relationship(back_populates='trajeto')

    # relacionamento N pontos de trajeto para 1 trajeto
    # cada trajeto pode ter vários pontos associados
    # ao ser cadastrado um novo ponto de trajeto nesse campo, ele se comunica com a coluna estrangeira da tabela trajeto
    trajeto_ponto: Mapped[list['PontoTrajeto']] = relationship()