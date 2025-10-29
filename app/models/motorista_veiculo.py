from sqlalchemy import Table, Column, ForeignKey
from config import db, Base

motorista_veiculo = Table(
  "motorista_veiculo",
  Base.metadata,
  Column("motorista_id", ForeignKey("motorista.id"), primary_key=True),
  Column("veiculo_id", ForeignKey("veiculo.id"), primary_key=True)
)