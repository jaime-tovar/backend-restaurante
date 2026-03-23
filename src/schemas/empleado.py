from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class EmpleadoBase(BaseModel):
    nombre_completo: str
    documento: str
    cargo: str
    email: EmailStr
    telefono: str
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    id_usuario_creacion: UUID


class EmpleadoUpdate(EmpleadoBase):
    nombre_completo: str | None = None
    documento: str | None = None
    cargo: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    activo: bool | None = None
    id_usuario_edita: UUID


class EmpleadoResponse(EmpleadoBase):
    id_empleado: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime | None

    class Config:
        from_attributes = True
