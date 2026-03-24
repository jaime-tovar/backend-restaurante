import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Plato(Base):
    __tablename__ = "platos"

    id_plato = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_categoria = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, default=True)

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
    categoria = relationship("Categoria", back_populates="platos")
    detalles = relationship(
        "DetalleOrden", back_populates="plato", cascade="all, delete-orphan"
    )
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
