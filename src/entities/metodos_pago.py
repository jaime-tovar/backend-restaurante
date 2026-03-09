import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class MetodoPago(Base):
    """
    Modelo que representa los métodos de pago disponibles
    en el sistema (efectivo, tarjeta, transferencia, etc.).
    """

    __tablename__ = "metodos_pago"

    id_metodo_pago = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    facturas = relationship("Factura", back_populates="metodo_pago")
