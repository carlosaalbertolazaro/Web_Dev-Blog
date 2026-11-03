from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Borrador(Base):
    __tablename__ = "borradores"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String(20), default="BORRADOR", nullable=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=True)
    fecha_publicacion = Column(DateTime(timezone=True), server_default=func.now())
    slug = Column(String(200), unique=True, nullable=False, index=True)
    estado = Column(String(20), default="PUBLICADO", nullable=False)