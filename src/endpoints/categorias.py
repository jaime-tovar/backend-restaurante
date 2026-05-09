from uuid import UUID

from datetime import timezone, datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
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
    categorias = db.query(Categoria).filter(Categoria.activo == True).all()
    data = [
        CategoriaResponse.model_validate(categoria).model_dump(mode="json")
        for categoria in categorias
    ]
    return success_response(data=data, message="Listado de categorías")


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    categoria = (
        db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    )

    if not categoria:
        raise NotFoundError("Categoría no encontrada")

    return success_response(data=categoria, message="Categoría encontrada")


@router.post("", response_model=CategoriaResponse, status_code=201)
def crear_categoria(dato: CategoriaCreate, db: Session = Depends(get_db)):
    if db.query(Categoria).filter(Categoria.nombre == dato.nombre).first():
        raise ConflictError(
            "El nombre de categoría ya está registrado", status_code=400
        )
    categoria = Categoria(
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
        activo=dato.activo,
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    data = CategoriaResponse.model_validate(categoria).model_dump(mode="json")
    return success_response(data=data, message="Categoría creada exitosamente")


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
        raise NotFoundError("Categoría no encontrada")
    update_data = dato.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return success_response(
        data=categoria, message="Categoría actualizada exitosamente"
    )


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    categoria = (
        db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    )
    if not categoria:
        raise NotFoundError("Categoría no encontrada")
    if categoria.fecha_eliminacion is not None:
        raise ConflictError("La categoría ya fue eliminada", status_code=400)
    categoria.fecha_eliminacion = datetime.now(timezone.utc)

    db.commit()
    db.refresh(categoria)

    return success_response(data=None, message="Categoría eliminada exitosamente")
