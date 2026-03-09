import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Reservacion(Base):
    """
    Modelo que representa las reservaciones del restaurante.

    Permite asociar un cliente a una mesa en una fecha
    determinada y controlar el estado de la reservación.
    """

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
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    cliente = relationship("Cliente", back_populates="reservaciones")
    mesa = relationship("Mesa", back_populates="reservaciones")
