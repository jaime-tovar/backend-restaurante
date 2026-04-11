from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.categoria import Categoria
from src.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
)

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    categoria = (
        db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    )

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return categoria


@router.post("", response_model=CategoriaResponse, status_code=201)
def crear_categoria(dato: CategoriaCreate, db: Session = Depends(get_db)):

    # validar que no exista el nombre
    existe = db.query(Categoria).filter(Categoria.nombre == dato.nombre).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe",
        )

    categoria = Categoria(
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
        activo=dato.activo,
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(
    categoria_id: UUID,
    dato: CategoriaUpdate,
    db: Session = Depends(get_db),
):

    categoria = (
        db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    )

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    update_data = dato.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):

    categoria = (
        db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    )

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    if not categoria.activo:
        raise HTTPException(status_code=400, detail="La categoría ya está inactiva")

    categoria.activo = False

    db.commit()

    return None
