from config import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Usuario(db.Model):
  __abstract__ = True

  id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
  cpf: Mapped[str] = mapped_column(String(14), unique=True)
  nome_completo: Mapped[str] = mapped_column(String(100))
  senha: Mapped[str] = mapped_column(String(30))
  role: Mapped[str] = mapped_column(String(20))