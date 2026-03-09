from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MetodoPagoBase(BaseModel):
    nombre: str
    activo: bool = True


class MetodoPagoCreate(MetodoPagoBase):
    pass


class MetodoPagoUpdate(MetodoPagoBase):
    nombre: str
    activo: bool


class MetodoPagoResponse(MetodoPagoBase):
    id_metodo_pago: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
