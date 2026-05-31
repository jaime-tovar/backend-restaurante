from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field


class DetalleOrdenBase(BaseModel):
    id_plato: UUID
    cantidad: int
    precio_unitario: Decimal


class DetalleOrdenCreate(BaseModel):
    id_plato: UUID
    cantidad: int = Field(gt=0)


class DetalleOrdenUpdate(BaseModel):
    id_orden: UUID | None = None
    id_plato: UUID | None = None
    cantidad: int | None = None
    precio_unitario: Decimal | None = None
    id_usuario_edita: UUID


class PlatoSimpleResponse(BaseModel):
    id_plato: UUID
    nombre: str
    precio: Decimal

    class Config:
        from_attributes = True


class DetalleOrdenResponse(BaseModel):

    id_detalle_orden: UUID
    id_orden: UUID
    cantidad: int
    precio_unitario: Decimal

    plato: PlatoSimpleResponse

    class Config:
        from_attributes = True
