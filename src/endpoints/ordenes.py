from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.orden import Orden
from src.entities.mesa import Mesa
from src.entities.plato import Plato
from src.entities.detalle_orden import DetalleOrden
from src.schemas.orden import (
    OrdenCreate,
    OrdenUpdate,
    OrdenResponse,
)
from src.schemas.detalle_orden import DetalleOrdenCreate

router = APIRouter(
    prefix="/ordenes", tags=["Ordenes"], dependencies=[Depends(get_current_user)]
)


@router.get("", dependencies=[Depends(get_current_user)])
def listar_ordenes(db: Session = Depends(get_db)):
    ordenes = db.query(Orden).filter(Orden.fecha_eliminacion.is_(None)).all()
    data = [
        OrdenResponse.model_validate(orden).model_dump(mode="json") for orden in ordenes
    ]
    return success_response(data=data, message="Listado de ordenes")


@router.get("/{orden_id}", dependencies=[Depends(get_current_user)])
def obtener_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise NotFoundError(detail="Orden no encontrada")
    data = OrdenResponse.model_validate(orden).model_dump(mode="json")
    return success_response(data=data, message="Orden encontrada")


@router.get("/mesa/{id_mesa}/activa")
def obtener_orden_activa(id_mesa: UUID, db: Session = Depends(get_db)):

    orden = (
        db.query(Orden)
        .filter(
            Orden.id_mesa == id_mesa,
            Orden.estado == "pendiente",
            Orden.fecha_eliminacion.is_(None),
        )
        .first()
    )

    if not orden:
        raise NotFoundError(detail="La mesa no tiene orden activa")

    data = OrdenResponse.model_validate(orden).model_dump(mode="json")

    return success_response(data=data, message="Orden activa encontrada")


@router.post("")
def crear_orden(orden_data: OrdenCreate, db: Session = Depends(get_db)):
    mesa = (
        db.query(Mesa)
        .filter(Mesa.id_mesa == orden_data.id_mesa, Mesa.fecha_eliminacion.is_(None))
        .first()
    )

    if not mesa:
        raise NotFoundError(detail="Mesa no encontrada")

    if mesa.estado != "disponible":
        raise ConflictError(detail="La mesa no está disponible")

    nueva_orden = Orden(
        id_mesa=orden_data.id_mesa,
        estado="pendiente",
        id_usuario_creacion=orden_data.id_usuario_creacion,
    )

    db.add(nueva_orden)
    db.flush()

    # Agregar detalles de la orden
    for detalle in orden_data.detalles:

        plato = (
            db.query(Plato)
            .filter(Plato.id_plato == detalle.id_plato, Plato.activo.is_(True))
            .first()
        )

        if not plato:
            raise NotFoundError(detail=f"Plato {detalle.id_plato} no encontrado")

        nuevo_detalle = DetalleOrden(
            id_orden=nueva_orden.id_orden,
            id_plato=detalle.id_plato,
            cantidad=detalle.cantidad,
            precio_unitario=plato.precio,
            id_usuario_creacion=orden_data.id_usuario_creacion,
        )

        db.add(nuevo_detalle)

    # Actualizar el estado de la mesa a "ocupada"
    mesa.estado = "ocupada"

    db.commit()

    db.refresh(nueva_orden)

    return success_response(data=nueva_orden, message="Orden creada")


@router.put("/{orden_id}/detalles")
def actualizar_detalles_orden(
    orden_id: UUID, detalles: list[DetalleOrdenCreate], db: Session = Depends(get_db)
):

    orden = db.query(Orden).filter(Orden.id_orden == orden_id).first()

    if not orden:
        raise NotFoundError(detail="Orden no encontrada")

    # eliminar detalles actuales
    (db.query(DetalleOrden).filter(DetalleOrden.id_orden == orden_id).delete())

    # crear nuevos detalles
    for detalle in detalles:

        plato = (
            db.query(Plato)
            .filter(Plato.id_plato == detalle.id_plato, Plato.activo.is_(True))
            .first()
        )

        if not plato:
            raise NotFoundError(detail=f"Plato {detalle.id_plato} no encontrado")

        nuevo_detalle = DetalleOrden(
            id_orden=orden_id,
            id_plato=detalle.id_plato,
            cantidad=detalle.cantidad,
            precio_unitario=plato.precio,
            id_usuario_creacion=orden.id_usuario_creacion,
        )

        db.add(nuevo_detalle)

    db.commit()

    return success_response(data=None, message="Detalles actualizados")


@router.put("/{orden_id}", dependencies=[Depends(get_current_user)])
def actualizar_orden(
    orden_id: UUID, orden_data: OrdenUpdate, db: Session = Depends(get_db)
):
    orden = db.query(Orden).filter(Orden.id_orden == orden_id).first()
    if not orden:
        raise NotFoundError(detail="Orden no encontrada")
    update_data = orden_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(orden, key, value)
    db.commit()
    db.refresh(orden)
    return success_response(data=orden, message="Orden actualizada")


@router.delete("/{orden_id}", dependencies=[Depends(get_current_user)])
def eliminar_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id_orden == orden_id).first()
    if not orden:
        raise NotFoundError(detail="Orden no encontrada")
    if orden.fecha_eliminacion is not None:
        raise ConflictError(detail="La orden ya ha sido eliminada")
    orden.fecha_eliminacion = datetime.now(timezone.utc)
    orden.estado = "eliminada"
    db.commit()
    db.refresh(orden)
    return success_response(data=None, message="Orden eliminada")
