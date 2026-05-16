from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.metodo_pago import MetodoPago
from src.schemas.metodo_pago import (
    MetodoPagoCreate,
    MetodoPagoResponse,
    MetodoPagoUpdate,
)

router = APIRouter(
    prefix="/metodos_pago",
    tags=["Metodos de Pago"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", dependencies=[Depends(get_current_user)])
def listar_metodos_pago(db: Session = Depends(get_db)):
    metodos_pago = (
        db.query(MetodoPago).filter(MetodoPago.fecha_eliminacion.is_(None)).all()
    )
    data = [
        MetodoPagoResponse.model_validate(metodo_pago).model_dump(mode="json")
        for metodo_pago in metodos_pago
    ]
    return success_response(data=data, message="Listado de métodos de pago")


@router.get("/{metodo_pago_id}", dependencies=[Depends(get_current_user)])
def obtener_metodo_pago(metodo_pago_id: UUID, db: Session = Depends(get_db)):
    metodo_pago = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago:
        raise NotFoundError("Metodo de pago no encontrado")
    data = MetodoPagoResponse.model_validate(metodo_pago).model_dump(mode="json")
    return success_response(data=data, message="Metodo de pago encontrado")


@router.post("/", dependencies=[Depends(get_current_user)])
def crear_metodo_pago(metodo_pago: MetodoPagoCreate, db: Session = Depends(get_db)):
    # Verificar si el método de pago ya existe
    metodo_pago_existente = (
        db.query(MetodoPago).filter(MetodoPago.nombre == metodo_pago.nombre).first()
    )
    if metodo_pago_existente:
        raise ConflictError("El método de pago ya existe")
    nuevo_metodo_pago = MetodoPago(
        nombre=metodo_pago.nombre,
        id_usuario_creacion=metodo_pago.id_usuario_creacion,
        activo=metodo_pago.activo,
    )
    db.add(nuevo_metodo_pago)
    db.commit()
    db.refresh(nuevo_metodo_pago)
    return success_response(data=nuevo_metodo_pago, message="Método de pago creado")


@router.put("/{metodo_pago_id}", dependencies=[Depends(get_current_user)])
def actualizar_metodo_pago(
    metodo_pago_id: UUID, metodo_pago: MetodoPagoUpdate, db: Session = Depends(get_db)
):
    metodo_pago_db = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago_db:
        raise NotFoundError("Metodo de pago no encontrado")
    # Verificar si el nuevo nombre del método de pago ya existe en otro registro
    metodo_pago_existente = (
        db.query(MetodoPago).filter(MetodoPago.nombre == metodo_pago.nombre).first()
    )
    if metodo_pago_existente:
        raise ConflictError("El método de pago ya existe")
    for key, value in metodo_pago.model_dump().items():
        setattr(metodo_pago_db, key, value)
    db.commit()
    db.refresh(metodo_pago_db)
    return success_response(data=metodo_pago_db, message="Método de pago actualizado")


@router.delete("/{metodo_pago_id}", dependencies=[Depends(get_current_user)])
def eliminar_metodo_pago(metodo_pago_id: UUID, db: Session = Depends(get_db)):
    metodo_pago_db = (
        db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == metodo_pago_id).first()
    )
    if not metodo_pago_db:
        raise NotFoundError("Metodo de pago no encontrado")
    if metodo_pago_db.fecha_eliminacion is not None:
        raise NotFoundError("Metodo de pago ya fue eliminado")
    metodo_pago_db.activo = False
    metodo_pago_db.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(metodo_pago_db)
    return success_response(data=None, message="Método de pago eliminado")
