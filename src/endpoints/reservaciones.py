from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.reservacion import Reservacion
from src.schemas.reservacion import (
    ReservacionCreate,
    ReservacionUpdate,
    ReservacionResponse,
)

router = APIRouter(
    prefix="/reservaciones",
    tags=["Reservaciones"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ReservacionResponse])
def listar_reservaciones(db: Session = Depends(get_db)):
    reservaciones = db.query(Reservacion).all()
    data = [
        ReservacionResponse.model_validate(reservacion).model_dump(mode="json")
        for reservacion in reservaciones
    ]
    return success_response(data=data, message="Listado de reservaciones")


@router.get("/{reservacion_id}", response_model=ReservacionResponse)
def obtener_reservacion(reservacion_id: UUID, db: Session = Depends(get_db)):
    reservacion = (
        db.query(Reservacion)
        .filter(Reservacion.id_reservacion == reservacion_id)
        .first()
    )
    if not reservacion:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    data = ReservacionResponse.model_validate(reservacion).model_dump(mode="json")
    return success_response(data=data, message="Reservación encontrada")


@router.post("", response_model=ReservacionResponse, status_code=201)
def crear_reservacion(reservacion: ReservacionCreate, db: Session = Depends(get_db)):
    new_reservacion = Reservacion(**reservacion.model_dump())
    db.add(new_reservacion)
    db.commit()
    db.refresh(new_reservacion)
    return success_response(
        data=new_reservacion, message="Reservación creada exitosamente"
    )


@router.put("/{reservacion_id}", response_model=ReservacionResponse)
def actualizar_reservacion(
    reservacion_id: UUID, reservacion: ReservacionUpdate, db: Session = Depends(get_db)
):
    existing_reservacion = (
        db.query(Reservacion)
        .filter(Reservacion.id_reservacion == reservacion_id)
        .first()
    )
    if not existing_reservacion:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")

    for key, value in reservacion.model_dump(exclude_unset=True).items():
        setattr(existing_reservacion, key, value)

    db.commit()
    db.refresh(existing_reservacion)
    return existing_reservacion


@router.delete("/{reservacion_id}", status_code=204)
def eliminar_reservacion(reservacion_id: UUID, db: Session = Depends(get_db)):
    reservacion = (
        db.query(Reservacion)
        .filter(Reservacion.id_reservacion == reservacion_id)
        .first()
    )
    if not reservacion:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")

    if reservacion.fecha_eliminacion is not None:
        raise HTTPException(status_code=400, detail="La reservación ya fue eliminada")

    reservacion.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(reservacion)
    return success_response(data=None, message="Reservación eliminada exitosamente")
