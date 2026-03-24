from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)
from src.utils.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


@router.post("", response_model=UsuarioResponse, status_code=201)
def crear_usuario(dato: UsuarioCreate, db: Session = Depends(get_db)):

    # validar que no exista el correo
    existe = db.query(Usuario).filter(Usuario.email == dato.email).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )

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

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: UUID, dato: UsuarioUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in dato.model_dump(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.put("/{usuario_id}", status_code=204)
def desactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not usuario.activo:
        raise HTTPException(status_code=400, detail="El usuario ya está inactivo")

    usuario.activo = False

    db.commit()

    return None
