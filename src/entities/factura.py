import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Factura(Base):
    __tablename__ = "facturas"

    id_factura = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    id_orden = Column(
        UUID(as_uuid=True),
        ForeignKey("ordenes.id_orden"),
        nullable=False,
        unique=True,
    )

    id_cliente = Column(
        UUID(as_uuid=True), ForeignKey("clientes.id_cliente"), nullable=True
    )

    fecha_emision = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    subtotal = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), nullable=False, default=0)
    total = Column(Numeric(10, 2), nullable=False)

    id_metodo_pago = Column(
        UUID(as_uuid=True),
        ForeignKey("metodos_pago.id_metodo_pago"),
        nullable=False,
    )

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
    orden = relationship("Orden", back_populates="factura")
    metodo_pago = relationship("MetodoPago", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
