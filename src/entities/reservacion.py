import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Reservacion(Base):
    __tablename__ = "reservaciones"

    id_reservacion = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    id_cliente = Column(
        UUID(as_uuid=True),
        ForeignKey("clientes.id_cliente"),
        nullable=True,
    )

    id_mesa = Column(
        UUID(as_uuid=True),
        ForeignKey("mesas.id_mesa"),
        nullable=True,
    )

    fecha = Column(DateTime(timezone=True), nullable=False)
    estado = Column(String(20), nullable=True, default="pendiente")

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
    cliente = relationship("Cliente", back_populates="reservaciones")
    mesa = relationship("Mesa", back_populates="reservaciones")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
