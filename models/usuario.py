from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Usuario():
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    cpf: Mapped[str] = mapped_column(String(14), primary_key=True, unique=True)
    nome_completo: Mapped[str] = mapped_column(String(100))
    senha: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(20))