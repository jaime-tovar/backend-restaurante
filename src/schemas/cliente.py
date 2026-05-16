from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None = None
    activo: bool = True


class ClienteCreate(ClienteBase):
    id_usuario_creacion: UUID


class ClienteUpdate(ClienteBase):
    documento: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    activo: bool | None = None
    id_usuario_edita: UUID


class ClienteResponse(ClienteBase):
    id_cliente: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None = None

    class Config:
        from_attributes = True
