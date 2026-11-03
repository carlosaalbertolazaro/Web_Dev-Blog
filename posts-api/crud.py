from sqlalchemy.orm import Session
from models import Borrador, Post
from schemas import BorradorCreate, BorradorUpdate, PostCreate
from sqlalchemy import func


def generar_slug(titulo: str) -> str:
    """Convierte un título en un slug amigable para URL."""
    slug = titulo.lower().strip()
    slug = slug.replace(" ", "-")
    # Eliminar caracteres especiales simples
    import re
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    return slug


# --- Operaciones Borrador ---

def get_borradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Borrador).offset(skip).limit(limit).all()


def get_borrador(db: Session, borrador_id: int):
    return db.query(Borrador).filter(Borrador.id == borrador_id).first()


def create_borrador(db: Session, borrador: BorradorCreate):
    db_borrador = Borrador(
        titulo=borrador.titulo,
        contenido=borrador.contenido,
        categoria=borrador.categoria,
        estado="BORRADOR"
    )
    db.add(db_borrador)
    db.commit()
    db.refresh(db_borrador)
    return db_borrador


def update_borrador(db: Session, borrador_id: int, borrador: BorradorUpdate):
    db_borrador = get_borrador(db, borrador_id)
    if not db_borrador:
        return None
    update_data = borrador.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_borrador, key, value)
    db.commit()
    db.refresh(db_borrador)
    return db_borrador


def delete_borrador(db: Session, borrador_id: int):
    db_borrador = get_borrador(db, borrador_id)
    if not db_borrador:
        return None
    db.delete(db_borrador)
    db.commit()
    return db_borrador


# --- Operaciones Post ---

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def get_post_by_slug(db: Session, slug: str):
    return db.query(Post).filter(Post.slug == slug).first()


def create_post(db: Session, post: PostCreate, slug: str):
    db_post = Post(
        titulo=post.titulo,
        contenido=post.contenido,
        categoria=post.categoria,
        slug=slug,
        estado="PUBLICADO"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
    return db_post