from sqlalchemy import String
from config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Embarcado(db.Model):
  __tablename__ = "embarcado"

  id: Mapped[int] = mapped_column(auto_increment=True, primary_key=True)
  mac: Mapped[str] = mapped_column(String, unique=True, nullable=False)