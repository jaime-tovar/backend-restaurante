import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Factura(Base):
    """
    Modelo que representa la factura generada a partir de una orden.

    Contiene información financiera como subtotal,
    descuento y método de pago utilizado.
    """

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

    fecha_factura = Column(
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

    # Relaciones
    orden = relationship("Orden", back_populates="factura")
    metodo_pago = relationship("MetodoPago", back_populates="facturas")
