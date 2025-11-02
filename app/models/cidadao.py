from app.config import db
from typing import TYPE_CHECKING
from models.usuario import Usuario
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Cidadao(db.Model, Usuario):
  __tablename__ = 'cidadao'