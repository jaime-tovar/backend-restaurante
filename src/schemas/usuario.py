from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UsuarioBase(BaseModel):
    id_empleado: UUID
    username: str
    password: str
    rol: str
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    id_usuario_creacion: UUID


class UsuarioUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    rol: str | None = None
    activo: bool | None = None
    id_usuario_edita: UUID


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    rol: str
    activo: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime | None = None
    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None

    class Config:
        orm_mode = True
