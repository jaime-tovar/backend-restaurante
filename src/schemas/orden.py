from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from src.schemas.mesa import MesaSimpleResponse
from src.schemas.detalle_orden import DetalleOrdenCreate


class OrdenBase(BaseModel):
    id_mesa: UUID


class OrdenCreate(BaseModel):
    id_mesa: UUID
    id_usuario_creacion: UUID

    detalles: list[DetalleOrdenCreate]


class OrdenUpdate(OrdenBase):
    id_mesa: UUID | None = None
    id_usuario_edita: UUID


class OrdenResponse(OrdenBase):
    id_orden: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    mesa: MesaSimpleResponse

    class Config:
        from_attributes = True
