from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FacturaBase(BaseModel):
    subtotal: float
    descuento: float = 0.0
    total: float
    id_metodo_pago: UUID


class FacturaCreate(FacturaBase):
    id_orden: UUID
    id_cliente: UUID


class FacturaUpdate(FacturaBase):
    subtotal: float | None = None
    descuento: float | None = None
    total: float | None = None
    id_metodo_pago: UUID | None = None
    id_orden: UUID | None = None
    id_cliente: UUID | None = None
    id_usuario_edita: UUID


class FacturaResponse(FacturaBase):
    id_factura: UUID
    fecha_emision: datetime
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
