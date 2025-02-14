from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from database import Base


class Empresa(Base):
    __tablename__ = "empresas"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")


class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    class Periodicidade(str, Enum):
        MENSAL = "mensal"
        TRIMESTRAL = "trimestral"
        ANUAL = "anual"

    periodicidade = Column(SQLAlchemyEnum(Periodicidade), nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship(Empresa, back_populates="obrigacoes")
