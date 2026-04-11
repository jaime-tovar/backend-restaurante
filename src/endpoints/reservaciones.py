from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.reservacion import Reservacion
from src.schemas.reservacion import (
    ReservacionCreate,
    ReservacionUpdate,
    ReservacionResponse,
)

router = APIRouter(prefix="/reservaciones", tags=["Reservaciones"])


@router.get("", response_model=list[ReservacionResponse])
def listar_reservaciones(db: Session = Depends(get_db)):
    reservaciones = db.query(Reservacion).all()
    return reservaciones


@router.get("/{reservacion_id}", response_model=ReservacionResponse)
def obtener_reservacion(reservacion_id: UUID, db: Session = Depends(get_db)):
    reservacion = (
        db.query(Reservacion)
        .filter(Reservacion.id_reservacion == reservacion_id)
        .first()
    )
    if not reservacion:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    return reservacion


@router.post("", response_model=ReservacionResponse, status_code=201)
def crear_reservacion(reservacion: ReservacionCreate, db: Session = Depends(get_db)):
    new_reservacion = Reservacion(**reservacion.model_dump())
    db.add(new_reservacion)
    db.commit()
    db.refresh(new_reservacion)
    return new_reservacion


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
    db.delete(reservacion)
    db.commit()
    return None
