from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MetodoPagoBase(BaseModel):
    nombre: str
    activo: bool = True


class MetodoPagoCreate(MetodoPagoBase):
    id_usuario_creacion: UUID


class MetodoPagoUpdate(MetodoPagoBase):
    nombre: str | None = None
    activo: bool | None = None
    id_usuario_edita: UUID


class MetodoPagoResponse(MetodoPagoBase):
    id_metodo_pago: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    class Config:
        from_attributes = True
