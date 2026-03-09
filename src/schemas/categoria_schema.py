from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    descripcion: str
    activo: bool = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    descripcion: str
    activo: bool


class CategoriaResponse(CategoriaBase):
    id_categoria: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    class Config:
        from_attributes = True
