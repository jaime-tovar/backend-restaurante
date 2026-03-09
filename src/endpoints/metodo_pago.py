from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.metodos_pago import MetodoPago
from src.schemas.metodo_pago_schema import (
    MetodoPagoCreate,
    MetodoPagoResponse,
    MetodoPagoUpdate,
)

router = APIRouter(prefix="/metodos_pago", tags=["Metodos de Pago"])


@router.get("", response_model=list[MetodoPagoResponse])
def listar_metodos_pago(db: Session = Depends(get_db)):
    return db.query(MetodoPago).all()


@router.get("/{metodo_pago_id}", response_model=MetodoPagoResponse)
def obtener_metodo_pago(metodo_pago_id: UUID, db: Session = Depends(get_db)):
    metodo_pago = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    return metodo_pago


@router.post("/", response_model=MetodoPagoResponse, status_code=201)
def crear_metodo_pago(metodo_pago: MetodoPagoCreate, db: Session = Depends(get_db)):

    # Verificar si el método de pago ya existe
    metodo_pago_existente = (
        db.query(MetodoPago).filter(MetodoPago.nombre == metodo_pago.nombre).first()
    )
    if metodo_pago_existente:
        raise HTTPException(status_code=400, detail="El método de pago ya existe")
    nuevo_metodo_pago = MetodoPago(**metodo_pago.model_dump())
    db.add(nuevo_metodo_pago)
    db.commit()
    db.refresh(nuevo_metodo_pago)
    return nuevo_metodo_pago


@router.put("/{metodo_pago_id}", response_model=MetodoPagoResponse)
def actualizar_metodo_pago(
    metodo_pago_id: UUID, metodo_pago: MetodoPagoUpdate, db: Session = Depends(get_db)
):
    metodo_pago_db = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago_db:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    # Verificar si el nuevo nombre del método de pago ya existe en otro registro
    metodo_pago_existente = (
        db.query(MetodoPago)
        .filter(
            MetodoPago.nombre == metodo_pago.nombre,
            MetodoPago.id_metodo_pago != metodo_pago_id,
        )
        .first()
    )
    if metodo_pago_existente:
        raise HTTPException(status_code=400, detail="El método de pago ya existe")
    for key, value in metodo_pago.model_dump().items():
        setattr(metodo_pago_db, key, value)
    db.commit()
    db.refresh(metodo_pago_db)
    return metodo_pago_db


@router.delete("/{metodo_pago_id}", status_code=204)
def eliminar_metodo_pago(metodo_pago_id: UUID, db: Session = Depends(get_db)):
    metodo_pago_db = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago_db:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    db.delete(metodo_pago_db)
    db.commit()
    return None
