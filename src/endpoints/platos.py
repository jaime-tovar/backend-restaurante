from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.plato import Plato
from src.schemas.plato import PlatoCreate, PlatoUpdate, PlatoResponse

router = APIRouter(
    prefix="/platos", tags=["Platos"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[PlatoResponse])
def get_platos(db: Session = Depends(get_db)):
    platos = db.query(Plato).all()
    return platos


@router.get("/{plato_id}", response_model=PlatoResponse)
def get_plato(plato_id: UUID, db: Session = Depends(get_db)):
    plato = db.query(Plato).filter(Plato.id_plato == plato_id).first()
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return plato


@router.post("", response_model=PlatoResponse)
def create_plato(plato: PlatoCreate, db: Session = Depends(get_db)):

    # Verificar si el plato ya existe
    existing_plato = db.query(Plato).filter(Plato.nombre == plato.nombre).first()
    if existing_plato:
        raise HTTPException(status_code=400, detail="El plato ya existe")
    new_plato = Plato(**plato.model_dump())
    db.add(new_plato)
    db.commit()
    db.refresh(new_plato)
    return new_plato


@router.put("/{plato_id}", response_model=PlatoResponse)
def update_plato(plato_id: UUID, plato: PlatoUpdate, db: Session = Depends(get_db)):
    existing_plato = db.query(Plato).filter(Plato.id_plato == plato_id).first()
    if not existing_plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    for key, value in plato.model_dump().items():
        setattr(existing_plato, key, value)
    db.commit()
    db.refresh(existing_plato)
    return existing_plato


@router.delete("/{plato_id}")
def delete_plato(plato_id: UUID, db: Session = Depends(get_db)):
    existing_plato = db.query(Plato).filter(Plato.id_plato == plato_id).first()
    if not existing_plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    db.delete(existing_plato)
    db.commit()
    return None
