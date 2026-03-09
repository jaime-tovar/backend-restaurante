from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PlatoBase(BaseModel):
    id_categoria: UUID
    nombre: str
    descripcion: str
    precio: float
    activo: bool = True


class PlatoCreate(PlatoBase):
    pass


class PlatoUpdate(PlatoBase):
    pass


class PlatoResponse(PlatoBase):
    id_plato: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
