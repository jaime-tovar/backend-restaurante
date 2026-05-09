from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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


@router.get("")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    data = [
        UsuarioResponse.model_validate(usuario).model_dump(mode="json")
        for usuario in usuarios
    ]
    return success_response(data=data, message="Listado de usuarios")


@router.get("/{usuario_id}")
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


@router.put("/{usuario_id}")
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


@router.put("/eliminar/{usuario_id}")
def desactivar_usuario(
    usuario_id: UUID, dato: UsuarioUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    if not usuario.activo:
        raise ConflictError("El usuario ya está inactivo")
    update = dato.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    db.commit()
    return success_response(message="Usuario desactivado exitosamente")
