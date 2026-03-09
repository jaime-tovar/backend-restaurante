"""
CRUD de mesa: conexión con los endpoints /mesas.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_mesas():
    """Lista todas las mesas."""
    return _get("/mesas")


def obtener_mesa(mesa_id):
    """Obtiene una mesa por su ID."""
    return _get(f"/mesas/{mesa_id}")


def crear_mesa(numero_mesa: int, capacidad: int, estado: str = "disponible") -> dict:
    """Crea una nueva mesa."""
    payload = {"numero_mesa": numero_mesa, "capacidad": capacidad, "estado": estado}
    return _post("/mesas", json=payload)


def actualizar_mesa(mesa_id, numero_mesa: int, capacidad: int, estado: str) -> dict:
    """Actualiza una mesa existente."""
    payload = {"numero_mesa": numero_mesa, "capacidad": capacidad, "estado": estado}
    return _put(f"/mesas/{mesa_id}", json=payload)


def eliminar_mesa(mesa_id):
    """Elimina una mesa por su ID."""
    return _delete(f"/mesas/{mesa_id}")
