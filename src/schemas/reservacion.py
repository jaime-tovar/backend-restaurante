from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReservacionBase(BaseModel):
    id_cliente: UUID
    id_mesa: UUID
    fecha: datetime
    estado: str = "pendiente"


class ReservacionCreate(ReservacionBase):
    id_usuario_creacion: UUID


class ReservacionUpdate(ReservacionBase):
    id_cliente: UUID | None = None
    id_mesa: UUID | None = None
    fecha: datetime | None = None
    estado: str | None = None
    id_usuario_edita: UUID


class ReservacionResponse(ReservacionBase):
    id_reservacion: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
