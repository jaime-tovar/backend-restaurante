import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Empleado(Base):
    __tablename__ = "empleado"

    id_empleado = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_completo = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    cargo = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Auditoría
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    # Relaciones
    usuario = relationship("Usuario", back_populates="empleado", uselist=False)
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
