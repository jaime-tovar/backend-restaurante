from uuid import UUID
from datetime import timezone, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.cliente import Cliente
from src.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(
    prefix="/clientes", tags=["clientes"], dependencies=[Depends(get_current_user)]
)


@router.get("", dependencies=[Depends(get_current_user)])
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).filter(Cliente.fecha_eliminacion.is_(None)).all()
    data = [
        ClienteResponse.model_validate(cliente).model_dump(mode="json")
        for cliente in clientes
    ]
    return success_response(data=data, message="Listado de clientes")


@router.get("/{cliente_id}", dependencies=[Depends(get_current_user)])
def obtener_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()
    if not cliente:
        raise NotFoundError("Cliente no encontrado")
    data = ClienteResponse.model_validate(cliente).model_dump(mode="json")
    return success_response(data=data, message="Cliente encontrado")


@router.post("", dependencies=[Depends(get_current_user)])
def crear_cliente(dato: ClienteCreate, db: Session = Depends(get_db)):
    # validar que no exista el correo
    existe = db.query(Cliente).filter(Cliente.email == dato.email).first()

    if existe:
        raise ConflictError("El cliente ya existe")

    cliente = Cliente(
        documento=dato.documento,
        nombre=dato.nombre,
        apellido=dato.apellido,
        email=dato.email,
        telefono=dato.telefono,
        activo=dato.activo,
        id_usuario_creacion=dato.id_usuario_creacion,
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    data = ClienteResponse.model_validate(cliente).model_dump(mode="json")
    return success_response(data=data, message="Cliente creado exitosamente")


@router.put("/{cliente_id}", dependencies=[Depends(get_current_user)])
def actualizar_cliente(
    cliente_id: UUID, dato: ClienteUpdate, db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()
    if not cliente:
        raise NotFoundError("Cliente no encontrado")
    update = dato.model_dump(exclude_unset=True)
    # validar que no exista el correo
    if "email" in update:
        existe = (
            db.query(Cliente)
            .filter(Cliente.email == update["email"], Cliente.id_cliente != cliente_id)
            .first()
        )
        if existe:
            raise ConflictError("El correo ya está en uso por otro cliente")
    for key, value in update.items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    data = ClienteResponse.model_validate(cliente).model_dump(mode="json")
    return success_response(data=data, message="Cliente actualizado exitosamente")


@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()
    if not cliente:
        raise NotFoundError("Cliente no encontrado")
    # Validar si ya fue eliminado
    if cliente.fecha_eliminacion is not None:
        raise ConflictError("El cliente ya ha sido eliminado")
    cliente.activo = False
    cliente.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(cliente)
    return success_response(data=None, message="Cliente eliminado exitosamente")
