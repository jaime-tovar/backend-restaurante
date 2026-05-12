import uuid

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Cliente(Base):
    __tablename__ = "clientes"

    # Columnas de la tabla
    id_cliente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    documento = Column(String(20), nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    email = Column(String(30), nullable=True)
    telefono = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)

    # Auditoría
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_eliminacion = Column(DateTime(timezone=True), nullable=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    # Relaciones
    reservaciones = relationship("Reservacion", back_populates="cliente")
    facturas = relationship("Factura", back_populates="cliente")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
