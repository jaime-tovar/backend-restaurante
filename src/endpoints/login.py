from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.core.auth import create_access_token
from src.core.config import get_settings
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.login import Login
from src.utils.security import verify_password


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/login")
def login(dato: Login, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == dato.username).first()
    if not user:
        raise NotFoundError("Usuario no encontrado")
    if not verify_password(dato.password, user.password):
        raise ConflictError("Contraseña no válida para el usuario", status_code=401)
    if not user.activo:
        raise ConflictError(
            "Usuario inactivo, contacte al administrador", status_code=403
        )

    settings = get_settings()
    access_token = create_access_token(
        subject=user.id_usuario,
        username=user.username,
        rol=user.rol,
        settings=settings,
    )

    data = {
        "resultado": "Login exitoso",
        "id_usuario": str(user.id_usuario),
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "rol": user.rol,
    }

    return success_response(data=data, message="Login exitoso")
