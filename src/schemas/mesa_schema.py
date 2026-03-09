from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MesaBase(BaseModel):
    numero_mesa: int
    capacidad: int
    estado: str = "disponible"


class MesaCreate(MesaBase):
    pass


class MesaUpdate(MesaBase):
    pass


class MesaResponse(MesaBase):
    id_mesa: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
