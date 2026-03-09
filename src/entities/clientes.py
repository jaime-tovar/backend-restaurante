import uuid

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Cliente(Base):
    """
    Modelo que representa a los clientes del sistema.

    Almacena la información básica de identificación
    y contacto del cliente.
    """

    __tablename__ = "clientes"

    id_cliente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    documento = Column(String(20), nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    email = Column(String(30), nullable=True)
    telefono = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    reservaciones = relationship("Reservacion", back_populates="cliente")
    ordenes = relationship("Orden", back_populates="cliente")
