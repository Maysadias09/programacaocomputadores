from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Opcao(Base):
    __tablename__ = 'opcoes'
    
    idOpcoes = Column(Integer, primary_key=True, autoincrement=True)
    textoOpcao = Column(String(45), nullable=False)
    votacoes_idVotacoes = Column(Integer, ForeignKey('votacoes.idVotacoes'))

    # Relacionamentos
    votacao = relationship("Votacao", back_populates="opcoes")
    votos = relationship("Voto", back_populates="opcao")

class Votacao(Base):
    __tablename__ = 'votacoes'
    
    idVotacoes = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(45), nullable=False)
    descricao = Column(String(45))
    dataCriacao = Column(DateTime)
    prazo_final = Column(DateTime)
    status = Column(String(45)) # Ex: "ATIVA", "ENCERRADA"

    # Relacionamentos
    opcoes = relationship("Opcao", back_populates="votacao")
    votos = relationship("Voto", back_populates="votacao")

class Voto(Base):
    __tablename__ = 'votos'
    
    idVotos = Column(Integer, primary_key=True, autoincrement=True)
    matriculaUsuario = Column(String(45), nullable=False)
    votacoes_idVotacoes = Column(Integer, ForeignKey('votacoes.idVotacoes'))
    opcoes_idOpcoes = Column(Integer, ForeignKey('opcoes.idOpcoes'))

    # Relacionamentos
    votacao = relationship("Votacao", back_populates="votos")
    opcao = relationship("Opcao", back_populates="votos")