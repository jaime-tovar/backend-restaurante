import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Categoria(Base):
    __tablename__ = "categorias"

    # Columnas de la tabla
    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    descripcion = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True)

    # Auditoría
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_eliminacion = Column(DateTime(timezone=True), nullable=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    # Relaciones
    platos = relationship("Plato", back_populates="categoria")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
