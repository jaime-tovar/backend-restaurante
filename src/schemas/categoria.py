from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    descripcion: str
    activo: bool = True


class CategoriaCreate(CategoriaBase):
    id_usuario_creacion: UUID


class CategoriaUpdate(CategoriaBase):
    descripcion: str | None = None
    activo: bool | None = None
    id_usuario_edita: UUID


class CategoriaResponse(CategoriaBase):
    id_categoria: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    class Config:
        from_attributes = True


class CategoriaSimpleResponse(BaseModel):
    id_categoria: UUID
    descripcion: str

    class Config:
        from_attributes = True
