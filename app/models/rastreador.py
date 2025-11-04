from typing import TYPE_CHECKING
from sqlalchemy import String
from config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
  from models.veiculo import Veiculo
  
class Rastreador(db.Model):
  __tablename__ = "rastreador"

  id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
  mac: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  
  veiculo: Mapped['Veiculo'] = relationship("Veiculo", back_populates="rastreador", uselist=False)