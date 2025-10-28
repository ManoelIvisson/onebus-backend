from app.config import db
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from models.motorista import Motorista
    from models.trajeto import Trajeto

class Veiculo(db.Model):
    __tablename__ = 'veiculo'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    placa: Mapped[str] = mapped_column(String(7), unique=True)
    tipo_veiculo: Mapped[str] = mapped_column(String(20))

    # relacionamento N motoristas para 1 carro
    # cada carro pode ter vários motoristas associados
    # ao ser cadastrado um novo motorista nesse campo, ele se comunica com a coluna estrangeira da tabela motorista
    motorista_cnh: Mapped[list['Motorista']] = relationship()

    # relacionamento N trajetos de viagem para 1 carro
    # cada carro pode ter vários trajetos associados
    # ao ser cadastrado um novo trajeto nesse campo, ele se comunica com a coluna estrangeira da tabela trajeto
    trajeto: Mapped[list['Trajeto']] = relationship()