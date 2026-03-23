import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_empleado = Column(
        UUID(as_uuid=True),
        ForeignKey("empleado.id_empleado"),
        nullable=False,
        unique=True,
    )
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)

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
    empleado = relationship("Empleado", back_populates="usuario")
    usuario_creacion = relationship(
        "Usuario", remote_side=[id_usuario], foreign_keys=[id_usuario_creacion]
    )

    usuario_edita = relationship(
        "Usuario", remote_side=[id_usuario], foreign_keys=[id_usuario_edita]
    )
