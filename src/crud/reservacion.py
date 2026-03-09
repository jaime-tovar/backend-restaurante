"""
CRUD de reservación: conexión con los endpoints /reservaciones.
"""

from datetime import datetime

from src.crud.client import _delete, _get, _post, _put


def listar_reservaciones():
    """Lista todas las reservaciones."""
    return _get("/reservaciones")


def obtener_reservacion(reservacion_id):
    """Obtiene una reservación por su ID."""
    return _get(f"/reservaciones/{reservacion_id}")


def crear_reservacion(
    id_cliente: str, id_mesa: str, fecha: datetime, estado: str = "pendiente"
) -> dict:
    """Crea una nueva reservación."""
    payload = {
        "id_cliente": id_cliente,
        "id_mesa": id_mesa,
        "fecha": fecha,
        "estado": estado,
    }
    return _post("/reservaciones", json=payload)


def actualizar_reservacion(reservacion_id: str, fecha: datetime, estado: str) -> dict:
    """Actualiza el estado de una reservación existente."""
    payload = {
        "fecha": fecha,
        "estado": estado,
    }
    return _put(f"/reservaciones/{reservacion_id}", json=payload)


def eliminar_reservacion(reservacion_id: str) -> dict:
    """Elimina una reservación por su ID."""
    return _delete(f"/reservaciones/{reservacion_id}")
