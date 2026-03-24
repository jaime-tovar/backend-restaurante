from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrdenBase(BaseModel):
    id_mesa: UUID
    estado: str = "pendiente"


class OrdenCreate(OrdenBase):
    id_usuario_creacion: UUID


class OrdenUpdate(OrdenBase):
    id_mesa: UUID | None = None
    estado: str | None = None
    id_usuario_edita: UUID


class OrdenResponse(OrdenBase):
    id_orden: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
