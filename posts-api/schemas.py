from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Esquemas para Borrador ---

class BorradorBase(BaseModel):
    titulo: str
    contenido: str
    categoria: Optional[str] = None


class BorradorCreate(BorradorBase):
    pass


class BorradorUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    categoria: Optional[str] = None


class BorradorOut(BorradorBase):
    id: int
    fecha_creacion: datetime
    estado: str

    class Config:
        from_attributes = True


# --- Esquemas para Post ---

class PostBase(BaseModel):
    titulo: str
    contenido: str
    categoria: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    fecha_publicacion: datetime
    slug: str
    estado: str

    class Config:
        from_attributes = True