from typing import TYPE_CHECKING
from sqlalchemy import String
from config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
  from models.veiculo import Veiculo
  
class Embarcado(db.Model):
  __tablename__ = "embarcado"

  id: Mapped[int] = mapped_column(auto_increment=True, primary_key=True)
  nome: Mapped[str] = mapped_column(String, unique=True)
  mac: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  
  veiculo: Mapped['Veiculo'] = relationship("Veiculo", back_populates="embarcado", uselist=False)