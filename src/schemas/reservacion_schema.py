from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReservacionBase(BaseModel):
    id_cliente: UUID
    id_mesa: UUID
    fecha: datetime
    estado: str = "pendiente"


class ReservacionCreate(ReservacionBase):
    pass


class ReservacionUpdate(ReservacionBase):
    pass


class ReservacionResponse(ReservacionBase):
    id_reservacion: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
