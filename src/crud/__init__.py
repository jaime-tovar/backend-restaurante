"""
Cliente CRUD que llama a los endpoints de la API (lógica Restaurante).
Nombres alineados con entities: categoria, cliente, detalle_orden, factura, mesa, metodo_pago, orden, plato, reservacion, usuario.
La API debe estar corriendo (uvicorn src.app:app --port 8000).
"""

from src.crud.usuario import (
    listar_usuarios,
    crear_usuario,
    obtener_usuario,
    actualizar_usuario,
    desactivar_usuario,
)

from src.crud.login import login

__all__ = [
    "listar_usuarios",
    "crear_usuario",
    "obtener_usuario",
    "actualizar_usuario",
    "desactivar_usuario",
    "login",
]
