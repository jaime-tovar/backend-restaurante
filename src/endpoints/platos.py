from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.plato import Plato
from src.schemas.plato import PlatoCreate, PlatoUpdate, PlatoResponse

router = APIRouter(
    prefix="/platos", tags=["Platos"], dependencies=[Depends(get_current_user)]
)


@router.get("", dependencies=[Depends(get_current_user)])
def listar_platos(db: Session = Depends(get_db)):
    platos = (
        db.query(Plato)
        .options(joinedload(Plato.categoria))
        .filter(Plato.fecha_eliminacion.is_(None))
        .all()
    )
    data = [
        PlatoResponse.model_validate(plato).model_dump(mode="json") for plato in platos
    ]
    return success_response(data, message="Listado de platos")


@router.get("/{plato_id}", dependencies=[Depends(get_current_user)])
def obtener_plato(plato_id: UUID, db: Session = Depends(get_db)):
    plato = (
        db.query(Plato)
        .options(joinedload(Plato.categoria))
        .filter(Plato.id_plato == plato_id, Plato.fecha_eliminacion.is_(None))
        .first()
    )
    if not plato:
        raise NotFoundError(detail="Plato no encontrado")
    data = PlatoResponse.model_validate(plato).model_dump(mode="json")
    return success_response(data, message="Plato encontrado")


@router.post("", dependencies=[Depends(get_current_user)])
def crear_plato(dato: PlatoCreate, db: Session = Depends(get_db)):
    if (
        db.query(Plato)
        .filter(
            Plato.nombre == dato.nombre,
        )
        .first()
    ):
        raise ConflictError(detail="El plato ya existe")
    plato = Plato(
        id_categoria=dato.id_categoria,
        nombre=dato.nombre,
        descripcion=dato.descripcion,
        precio=dato.precio,
        activo=dato.activo,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(plato)
    db.commit()
    db.refresh(plato)
    return success_response(plato, message="Plato creado exitosamente")


@router.put("/{plato_id}", dependencies=[Depends(get_current_user)])
def actualizar_plato(plato_id: UUID, dato: PlatoUpdate, db: Session = Depends(get_db)):
    plato = db.query(Plato).filter(Plato.id_plato == plato_id).first()
    if not plato:
        raise NotFoundError(detail="Plato no encontrado")
    update_data = dato.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plato, key, value)
    db.commit()
    db.refresh(plato)
    return success_response(plato, message="Plato actualizado exitosamente")


@router.delete("/{plato_id}", dependencies=[Depends(get_current_user)])
def eliminar_plato(plato_id: UUID, db: Session = Depends(get_db)):
    plato = db.query(Plato).filter(Plato.id_plato == plato_id).first()
    if not plato:
        raise NotFoundError(detail="Plato no encontrado")
    if plato.fecha_eliminacion is not None:
        raise ConflictError(detail="El plato ya ha sido eliminado")
    plato.fecha_eliminacion = datetime.now(timezone.utc)
    plato.activo = False
    db.commit()
    db.refresh(plato)
    return success_response(None, message="Plato eliminado exitosamente")
