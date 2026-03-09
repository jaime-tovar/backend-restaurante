from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrdenBase(BaseModel):
    id_mesa: UUID
    id_cliente: UUID | None
    estado: str = "pendiente"


class OrdenCreate(OrdenBase):
    pass


class OrdenUpdate(BaseModel):
    pass


class OrdenResponse(OrdenBase):
    id_orden: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
