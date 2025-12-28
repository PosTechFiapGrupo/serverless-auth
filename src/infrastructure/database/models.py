from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomerModel(Base):
    """
    Customer database model.

    Maps to the 'clientes' table in MySQL.
    Follows production database schema.
    """

    __tablename__ = "clientes"

    id = Column(String(36), primary_key=True)
    cpf = Column(String(14), unique=True, nullable=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Customer(id={self.id}, cpf={self.cpf}, nome={self.nome})>"
