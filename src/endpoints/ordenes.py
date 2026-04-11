from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.orden import Orden
from src.schemas.orden import (
    OrdenCreate,
    OrdenUpdate,
    OrdenResponse,
)

router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


@router.get("", response_model=list[OrdenResponse])
def listar_ordenes(db: Session = Depends(get_db)):
    return db.query(Orden).all()


@router.get("/{orden_id}", response_model=OrdenResponse)
def obtener_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden


@router.post("", response_model=OrdenResponse, status_code=201)
def crear_orden(orden_data: OrdenCreate, db: Session = Depends(get_db)):

    # Verificar si la orden ya existe
    orden_existente = (
        db.query(Orden).filter(Orden.id_orden == orden_data.orden_id).first()
    )
    if orden_existente:
        raise HTTPException(status_code=400, detail="La orden ya existe")
    nueva_orden = Orden(**orden_data.model_dump())
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden


@router.put("/{orden_id}", response_model=OrdenResponse)
def actualizar_orden(
    orden_id: UUID, orden_data: OrdenUpdate, db: Session = Depends(get_db)
):
    orden = db.query(Orden).filter(Orden.id_orden == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    for key, value in orden_data.model_dump(exclude_unset=True).items():
        setattr(orden, key, value)
    db.commit()
    db.refresh(orden)
    return orden


@router.delete("/{orden_id}", status_code=204)
def eliminar_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id_orden == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    db.delete(orden)
    db.commit()
