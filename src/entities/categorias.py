import uuid

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Categoria(Base):
    """
    Modelo que representa las categorías de los platos.

    Permite clasificar los platos dentro del sistema
    (por ejemplo: bebidas, entradas, postres, etc.).
    """

    __tablename__ = "categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    descripcion = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    platos = relationship("Plato", back_populates="categoria")
