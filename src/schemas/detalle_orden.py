from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class DetalleOrdenBase(BaseModel):
    id_orden: UUID
    id_plato: UUID
    cantidad: int
    precio_unitario: Decimal


class DetalleOrdenCreate(DetalleOrdenBase):
    id_usuario_creacion: UUID


class DetalleOrdenUpdate(DetalleOrdenBase):
    id_orden: UUID | None = None
    id_plato: UUID | None = None
    cantidad: int | None = None
    precio_unitario: Decimal | None = None
    id_usuario_edita: UUID


class DetalleOrdenResponse(DetalleOrdenBase):
    id_detalle_orden: UUID

    class Config:
        from_attributes = True
