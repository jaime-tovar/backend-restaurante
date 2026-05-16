from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.mesa import Mesa
from src.schemas.mesa import MesaCreate, MesaUpdate, MesaResponse

router = APIRouter(
    prefix="/mesas", tags=["Mesas"], dependencies=[Depends(get_current_user)]
)


@router.get("", dependencies=[Depends(get_current_user)])
def listar_mesas(db: Session = Depends(get_db)):
    mesas = db.query(Mesa).filter(Mesa.fecha_eliminacion.is_(None)).all()
    data = [MesaResponse.model_validate(mesa).model_dump(mode="json") for mesa in mesas]
    return success_response(data=data, message="Listado de mesas")


@router.get("/{mesa_id}", dependencies=[Depends(get_current_user)])
def obtener_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise NotFoundError(detail="Mesa no encontrada")
    data = MesaResponse.model_validate(mesa).model_dump(mode="json")
    return success_response(data=data, message="Mesa encontrada")


@router.post("/", dependencies=[Depends(get_current_user)])
def crear_mesa(mesa: MesaCreate, db: Session = Depends(get_db)):
    existe = (
        db.query(Mesa)
        .filter(Mesa.numero_mesa == mesa.numero_mesa, Mesa.fecha_eliminacion.is_(None))
        .first()
    )
    if existe:
        raise ConflictError(detail="El número de mesa ya existe")
    nueva_mesa = Mesa(
        numero_mesa=mesa.numero_mesa,
        capacidad=mesa.capacidad,
        estado=mesa.estado,
        id_usuario_creacion=mesa.id_usuario_creacion,
    )
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return success_response(data=nueva_mesa, message="Mesa creada")


@router.put("/{mesa_id}", dependencies=[Depends(get_current_user)])
def actualizar_mesa(mesa_id: UUID, mesa: MesaUpdate, db: Session = Depends(get_db)):
    mesa_db = db.query(Mesa).filter(Mesa.id_mesa == mesa_id).first()
    if not mesa_db:
        raise NotFoundError(detail="Mesa no encontrada")
    if mesa.numero_mesa != mesa_db.numero_mesa:
        existe = db.query(Mesa).filter(Mesa.numero_mesa == mesa.numero_mesa).first()
        if existe:
            raise ConflictError(detail="El número de mesa ya existe")
    for key, value in mesa.model_dump().items():
        setattr(mesa_db, key, value)
    db.commit()
    db.refresh(mesa_db)
    return success_response(data=mesa_db, message="Mesa actualizada")


@router.delete("/{mesa_id}", dependencies=[Depends(get_current_user)])
def eliminar_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    mesa_db = db.query(Mesa).filter(Mesa.id_mesa == mesa_id).first()
    if not mesa_db:
        raise NotFoundError(detail="Mesa no encontrada")
    if mesa_db.fecha_eliminacion is not None:
        raise NotFoundError(detail="Mesa ya eliminada")
    mesa_db.estado = "eliminada"
    mesa_db.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(mesa_db)
    return success_response(data=None, message="Mesa eliminada")
