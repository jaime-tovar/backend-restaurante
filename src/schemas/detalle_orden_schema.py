from uuid import UUID

from pydantic import BaseModel


class DetalleOrdenBase(BaseModel):
    id_orden: UUID
    id_plato: UUID
    cantidad: int
    precio_unitario: float


class DetalleOrdenCreate(DetalleOrdenBase):
    pass


class DetalleOrdenUpdate(DetalleOrdenBase):
    pass


class DetalleOrdenResponse(DetalleOrdenBase):
    id_detalle_orden: UUID

    class Config:
        from_attributes = True
