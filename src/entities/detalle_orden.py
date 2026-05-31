import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class DetalleOrden(Base):
    __tablename__ = "detalle_orden"

    id_detalle_orden = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    id_orden = Column(
        UUID(as_uuid=True),
        ForeignKey("ordenes.id_orden"),
        nullable=False,
    )

    id_plato = Column(
        UUID(as_uuid=True),
        ForeignKey("platos.id_plato"),
        nullable=False,
    )

    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
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
    orden = relationship("Orden", back_populates="detalles")
    plato = relationship("Plato", back_populates="detalles")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
