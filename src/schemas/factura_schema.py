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
    pass


class FacturaUpdate(FacturaBase):
    pass


class FacturaResponse(FacturaBase):
    id_factura: UUID
    fecha_factura: datetime

    class Config:
        from_attributes = True
