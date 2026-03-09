from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.mesas import Mesa
from src.schemas.mesa_schema import MesaCreate, MesaUpdate, MesaResponse

router = APIRouter(prefix="/mesas", tags=["Mesas"])


@router.get("", response_model=list[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    mesas = db.query(Mesa).all()
    return mesas


@router.get("/{mesa_id}", response_model=MesaResponse)
def obtener_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.post("/", response_model=MesaResponse)
def crear_mesa(mesa: MesaCreate, db: Session = Depends(get_db)):
    existe = db.query(Mesa).filter(Mesa.numero_mesa == mesa.numero_mesa).first()
    if existe:
        raise HTTPException(status_code=400, detail="El número de mesa ya existe")
    nueva_mesa = Mesa(**mesa.model_dump())
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa


@router.put("/{mesa_id}", response_model=MesaResponse)
def actualizar_mesa(mesa_id: UUID, mesa: MesaUpdate, db: Session = Depends(get_db)):
    mesa_db = db.query(Mesa).filter(Mesa.id_mesa == mesa_id).first()
    if not mesa_db:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    if mesa.numero_mesa != mesa_db.numero_mesa:
        existe = db.query(Mesa).filter(Mesa.numero_mesa == mesa.numero_mesa).first()
        if existe:
            raise HTTPException(status_code=400, detail="El número de mesa ya existe")
    for key, value in mesa.model_dump().items():
        setattr(mesa_db, key, value)
    db.commit()
    db.refresh(mesa_db)
    return mesa_db


@router.delete("/{mesa_id}")
def eliminar_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    mesa_db = db.query(Mesa).filter(Mesa.id_mesa == mesa_id).first()
    if not mesa_db:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    db.delete(mesa_db)
    db.commit()
    return {"detail": "Mesa eliminada"}
