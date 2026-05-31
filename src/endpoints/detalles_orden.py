from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.detalle_orden import DetalleOrden
from src.schemas.detalle_orden import (
    DetalleOrdenCreate,
    DetalleOrdenUpdate,
    DetalleOrdenResponse,
)

router = APIRouter(
    prefix="/detalle_orden",
    tags=["Detalle Orden"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/orden/{id_orden}", dependencies=[Depends(get_current_user)])
def listar_detalles_orden(id_orden: UUID, db: Session = Depends(get_db)):
    detalles_orden = (
        db.query(DetalleOrden).filter(DetalleOrden.id_orden == id_orden).all()
    )
    data = [
        DetalleOrdenResponse.model_validate(detalle).model_dump(mode="json")
        for detalle in detalles_orden
    ]
    return success_response(data=data, message="Listado de detalles de orden")


@router.get("/detalle/{id_detalle_orden}", dependencies=[Depends(get_current_user)])
def obtener_detalle_orden(id_detalle_orden: UUID, db: Session = Depends(get_db)):
    detalle_orden = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_detalle_orden == id_detalle_orden)
        .first()
    )
    if not detalle_orden:
        raise NotFoundError("Detalle de orden no encontrado")
    data = DetalleOrdenResponse.model_validate(detalle_orden).model_dump(mode="json")
    return success_response(data=data, message="Detalle de orden obtenido")


@router.post("", dependencies=[Depends(get_current_user)])
def crear_detalle_orden(
    detalle_orden: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    existe = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_orden == detalle_orden.id_orden)
        .filter(DetalleOrden.id_plato == detalle_orden.id_plato)
        .first()
    )
    if existe:
        raise ConflictError(detail="Ya existe un detalle para esta orden y plato")
    new_detalle_orden = DetalleOrden(**detalle_orden.model_dump())
    db.add(new_detalle_orden)
    db.commit()
    db.refresh(new_detalle_orden)
    return success_response(data=new_detalle_orden, message="Detalle de orden creado")


@router.put("/{id_detalle_orden}", dependencies=[Depends(get_current_user)])
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
        raise NotFoundError("Detalle de orden no encontrado")
    for key, value in detalle_orden_update.model_dump().items():
        setattr(detalle_orden, key, value)
    db.commit()
    db.refresh(detalle_orden)
    return success_response(data=detalle_orden, message="Detalle de orden actualizado")


@router.delete("/{id_detalle_orden}", dependencies=[Depends(get_current_user)])
def delete_detalle_orden(id_detalle_orden: UUID, db: Session = Depends(get_db)):
    detalle_orden = (
        db.query(DetalleOrden)
        .filter(DetalleOrden.id_detalle_orden == id_detalle_orden)
        .first()
    )
    if not detalle_orden:
        raise NotFoundError("Detalle de orden no encontrado")

    detalle_orden.activo = False
    detalle_orden.fecha_eliminacion = datetime.now(timezone.utc)

    db.commit()
    db.refresh(detalle_orden)
    return success_response(
        data=None, message="Detalle de orden eliminado exitosamente"
    )
