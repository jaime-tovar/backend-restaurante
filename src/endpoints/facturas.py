from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.facturas import Factura
from src.schemas.factura_schema import FacturaCreate, FacturaUpdate, FacturaResponse

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.get("", response_model=list[FacturaResponse])
def list_facturas(db: Session = Depends(get_db)):
    return db.query(Factura).all()


@router.get("/{factura_id}", response_model=FacturaResponse)
def get_factura(factura_id: UUID, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id_factura == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.post("/", response_model=FacturaResponse)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):

    existe = db.query(Factura).filter(Factura.id_orden == factura.id_orden).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe factura para esta orden")

    new_factura = Factura(**factura.model_dump())
    db.add(new_factura)
    db.commit()
    db.refresh(new_factura)
    return new_factura


@router.put("/{factura_id}", response_model=FacturaResponse)
def update_factura(
    factura_id: UUID, factura: FacturaUpdate, db: Session = Depends(get_db)
):
    existing_factura = (
        db.query(Factura).filter(Factura.id_factura == factura_id).first()
    )
    if not existing_factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    for key, value in factura.model_dump(exclude_unset=True).items():
        setattr(existing_factura, key, value)

    db.commit()
    db.refresh(existing_factura)
    return existing_factura


@router.delete("/{factura_id}", status_code=204)
def delete_factura(factura_id: UUID, db: Session = Depends(get_db)):
    existing_factura = (
        db.query(Factura).filter(Factura.id_factura == factura_id).first()
    )
    if not existing_factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    db.delete(existing_factura)
    db.commit()
