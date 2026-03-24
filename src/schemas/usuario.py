from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre_completo: str
    username: str
    email: EmailStr
    telefono: str
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str
    rol: str


class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    username: str | None = None
    password: str | None = None
    rol: str | None = None
    activo: bool | None = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    rol: str
    activo: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime | None = None

    class Config:
        from_attributes = True
