from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_validator
from src.schemas.categoria import CategoriaSimpleResponse


class PlatoBase(BaseModel):
    id_categoria: UUID
    nombre: str
    descripcion: str | None = None
    precio: Decimal
    activo: bool = True

    @field_validator("precio")
    def precio_valido(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v


class PlatoCreate(PlatoBase):
    id_usuario_creacion: UUID


class PlatoUpdate(PlatoBase):
    id_categoria: UUID | None = None
    nombre: str | None = None
    descripcion: str | None = None
    precio: Decimal | None = None
    activo: bool | None = None


class PlatoResponse(PlatoBase):
    id_plato: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    categoria: CategoriaSimpleResponse

    class Config:
        from_attributes = True
