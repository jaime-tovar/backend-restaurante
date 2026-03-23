from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.detalle_orden import DetalleOrden
from src.schemas.detalle_orden import (
    DetalleOrdenCreate,
    DetalleOrdenUpdate,
    DetalleOrdenResponse,
)

router = APIRouter(prefix="/detalle_orden", tags=["Detalle Orden"])


@router.get("", response_model=list[DetalleOrdenResponse])
def list_detalle_orden(db: Session = Depends(get_db)):
    return db.query(DetalleOrden).all()


@router.get("/{id_detalle_orden}", response_model=DetalleOrdenResponse)
def get_detalle_orden(id_detalle_orden: UUID, db: Session = Depends(get_db)):
    detalle_orden = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_detalle_orden == id_detalle_orden)
        .first()
    )
    if not detalle_orden:
        raise HTTPException(status_code=404, detail="Detalle de orden no encontrado")
    return detalle_orden


@router.post("/", response_model=DetalleOrdenResponse)
def create_detalle_orden(
    detalle_orden: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    existe = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_orden == detalle_orden.id_orden)
        .filter(DetalleOrden.id_plato == detalle_orden.id_plato)
        .first()
    )
    if existe:
        raise HTTPException(
            status_code=400, detail="Ya existe un detalle para esta orden y plato"
        )
    new_detalle_orden = DetalleOrden(**detalle_orden.model_dump())
    db.add(new_detalle_orden)
    db.commit()
    db.refresh(new_detalle_orden)
    return new_detalle_orden


@router.put("/{id_detalle_orden}", response_model=DetalleOrdenResponse)
def update_detalle_orden(
    id_detalle_orden: UUID,
    detalle_orden_update: DetalleOrdenUpdate,
    db: Session = Depends(get_db),
):
    detalle_orden = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_detalle_orden == id_detalle_orden)
        .first()
    )
    if not detalle_orden:
        raise HTTPException(status_code=404, detail="Detalle de orden no encontrado")
    for key, value in detalle_orden_update.model_dump().items():
        setattr(detalle_orden, key, value)
    db.commit()
    db.refresh(detalle_orden)
    return detalle_orden


@router.delete("/{id_detalle_orden}")
def delete_detalle_orden(id_detalle_orden: UUID, db: Session = Depends(get_db)):
    detalle_orden = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_detalle_orden == id_detalle_orden)
        .first()
    )
    if not detalle_orden:
        raise HTTPException(status_code=404, detail="Detalle de orden no encontrado")
    db.delete(detalle_orden)
    db.commit()
    return {"detail": "Detalle de orden eliminado exitosamente"}
