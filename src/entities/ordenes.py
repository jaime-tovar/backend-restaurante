import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Orden(Base):
    """
    Modelo que representa las órdenes realizadas en el restaurante.

    Cada orden está asociada a una mesa y opcionalmente
    a un cliente. Contiene la fecha en la que fue creada.
    """

    __tablename__ = "ordenes"

    id_orden = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_mesa = Column(UUID(as_uuid=True), ForeignKey("mesas.id_mesa"), nullable=False)
    id_cliente = Column(
        UUID(as_uuid=True), ForeignKey("clientes.id_cliente"), nullable=True
    )
    estado = Column(String(20), nullable=False, default="pendiente")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    mesa = relationship("Mesa", back_populates="ordenes")
    cliente = relationship("Cliente", back_populates="ordenes")

    detalles = relationship(
        "DetalleOrden", back_populates="orden", cascade="all, delete-orphan"
    )

    factura = relationship("Factura", back_populates="orden", uselist=False)
