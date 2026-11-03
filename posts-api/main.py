from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, crud

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="posts-api",
    description="API de administración de CMS para blog personal",
    version="1.0.0"
)


# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Endpoints de Borradores ----------

@app.get("/borradores", response_model=list[schemas.BorradorOut])
def listar_borradores(db: Session = Depends(get_db)):
    """Listar todos los borradores"""
    return crud.get_borradores(db)


@app.post("/borradores", response_model=schemas.BorradorOut, status_code=201)
def crear_borrador(borrador: schemas.BorradorCreate, db: Session = Depends(get_db)):
    """Crear un nuevo borrador"""
    if not borrador.titulo or not borrador.titulo.strip():
        raise HTTPException(status_code=422, detail="El título es obligatorio")
    return crud.create_borrador(db=db, borrador=borrador)


@app.get("/borradores/{borrador_id}", response_model=schemas.BorradorOut)
def obtener_borrador(borrador_id: int, db: Session = Depends(get_db)):
    """Obtener un borrador por su ID"""
    db_borrador = crud.get_borrador(db, borrador_id=borrador_id)
    if not db_borrador:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")
    return db_borrador


@app.put("/borradores/{borrador_id}", response_model=schemas.BorradorOut)
def editar_borrador(
    borrador_id: int,
    borrador: schemas.BorradorUpdate,
    db: Session = Depends(get_db)
):
    """Editar un borrador existente"""
    if borrador.titulo is not None and not borrador.titulo.strip():
        raise HTTPException(status_code=422, detail="El título no puede estar vacío")
    db_borrador = crud.update_borrador(db, borrador_id=borrador_id, borrador=borrador)
    if not db_borrador:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")
    return db_borrador


@app.delete("/borradores/{borrador_id}", status_code=204)
def eliminar_borrador(borrador_id: int, db: Session = Depends(get_db)):
    """Eliminar un borrador"""
    db_borrador = crud.delete_borrador(db, borrador_id=borrador_id)
    if not db_borrador:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")
    return None


@app.post("/borradores/{borrador_id}/publicar", response_model=schemas.PostOut, status_code=201)
def publicar_borrador(borrador_id: int, db: Session = Depends(get_db)):
    """
    Publicar un borrador: crea un Post nuevo y elimina el borrador original.
    Regla clave: el borrador NO se convierte en post, se crea uno nuevo.
    """
    db_borrador = crud.get_borrador(db, borrador_id=borrador_id)
    if not db_borrador:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")

    slug = crud.generar_slug(db_borrador.titulo)

    # Verificar que no exista ya un post con ese slug
    post_existente = crud.get_post_by_slug(db, slug=slug)
    if post_existente:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un post publicado con el slug '{slug}'"
        )

    # Crear el Post nuevo con los datos del borrador
    post_data = schemas.PostCreate(
        titulo=db_borrador.titulo,
        contenido=db_borrador.contenido,
        categoria=db_borrador.categoria
    )
    db_post = crud.create_post(db=db, post=post_data, slug=slug)

    # Eliminar el borrador original
    crud.delete_borrador(db, borrador_id=borrador_id)

    return db_post


# ---------- Endpoints de Posts ----------

@app.get("/posts", response_model=list[schemas.PostOut])
def listar_posts(db: Session = Depends(get_db)):
    """Listar todos los posts publicados"""
    return crud.get_posts(db)


@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def obtener_post(post_id: int, db: Session = Depends(get_db)):
    """Obtener un post por su ID"""
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return db_post


@app.delete("/posts/{post_id}", status_code=204)
def eliminar_post(post_id: int, db: Session = Depends(get_db)):
    """Eliminar un post publicado"""
    db_post = crud.delete_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return None