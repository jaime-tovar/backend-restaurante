from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MesaBase(BaseModel):
    numero_mesa: int
    capacidad: int
    estado: str = "disponible"


class MesaCreate(MesaBase):
    id_usuario_creacion: UUID


class MesaUpdate(MesaBase):
    numero_mesa: int | None = None
    capacidad: int | None = None
    estado: str | None = None
    id_usuario_edita: UUID


class MesaResponse(MesaBase):
    id_mesa: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
