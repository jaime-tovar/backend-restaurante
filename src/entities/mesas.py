import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Mesa(Base):
    """
    Modelo que representa las mesas del restaurante.

    Permite gestionar la disponibilidad, capacidad
    y estado actual de cada mesa.
    """

    __tablename__ = "mesas"

    id_mesa = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    numero_mesa = Column(Integer, nullable=False, unique=True)
    capacidad = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False, default="disponible")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    reservaciones = relationship("Reservacion", back_populates="mesa")
    ordenes = relationship("Orden", back_populates="mesa")
