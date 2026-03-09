import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class DetalleOrden(Base):
    """
    Modelo que representa el detalle de una orden.

    Cada registro indica qué plato pertenece a una orden
    y la cantidad solicitada.
    """

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

    # Relaciones
    orden = relationship("Orden", back_populates="detalles")
    plato = relationship("Plato", back_populates="detalles")
