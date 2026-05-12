from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)
from src.utils.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/existe")
def existe_usuario(db: Session = Depends(get_db)):
    existe = (
        db.query(Usuario).filter(Usuario.fecha_eliminacion.is_(None)).first()
        is not None
    )
    return success_response(data=existe, message="Validación de usuarios")


@router.get("", dependencies=[Depends(get_current_user)])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).filter(Usuario.fecha_eliminacion.is_(None)).all()
    data = [
        UsuarioResponse.model_validate(usuario).model_dump(mode="json")
        for usuario in usuarios
    ]
    return success_response(data=data, message="Listado de usuarios")


@router.get("/{usuario_id}", dependencies=[Depends(get_current_user)])
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario encontrado")


@router.post("", status_code=201)
def crear_usuario(dato: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.username == dato.username).first():
        raise ConflictError("El nombre de usuario ya está registrado", status_code=400)
    if db.query(Usuario).filter(Usuario.email == dato.email).first():
        raise ConflictError("El correo ya está registrado", status_code=400)
    usuario = Usuario(
        nombre_completo=dato.nombre_completo,
        email=dato.email,
        telefono=dato.telefono,
        username=dato.username,
        password=hash_password(dato.password),
        rol=dato.rol,
        activo=dato.activo,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario creado exitosamente")


@router.put("/{usuario_id}", dependencies=[Depends(get_current_user)])
def actualizar_usuario(
    usuario_id: UUID, dato: UsuarioUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if "password" in update and update["password"]:
        update["password"] = hash_password(update["password"])
    for key, value in update.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario actualizado exitosamente")


@router.delete("/{usuario_id}", dependencies=[Depends(get_current_user)])
def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    # Validar si ya fue eliminado
    if usuario.fecha_eliminacion is not None:
        raise ConflictError("El usuario ya fue eliminado", status_code=400)
    usuario.activo = False
    usuario.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(usuario)
    return success_response(data=None, message="Usuario eliminado exitosamente")
