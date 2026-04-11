from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
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
    if user.rol.lower() != "admin":
        raise ConflictError(
            "Acceso restringido, el usuario no es administrador", status_code=403
        )
    return success_response(
        data={"resultado": "Login exitoso", "id_usuario": user.id_usuario},
        message="Login exitoso",
    )
