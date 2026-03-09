"""
CRUD de orden: conexión con los endpoints /ordenes.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_ordenes():
    """Obtiene la lista de órdenes."""
    return _get("/ordenes")


def obtener_orden(id_orden):
    """Obtiene una orden por su ID."""
    return _get(f"/ordenes/{id_orden}")


def crear_orden(id_mesa: str, id_cliente: str, estado: str = "pendiente") -> dict:
    """Crea una nueva orden."""
    payload = {"id_mesa": id_mesa, "id_cliente": id_cliente, "estado": estado}
    return _post("/ordenes", json=payload)


def actualizar_orden(id_orden: str, id_mesa: str, id_cliente: str, estado: str) -> dict:
    """Actualiza una orden existente."""
    payload = {"id_mesa": id_mesa, "id_cliente": id_cliente, "estado": estado}
    return _put(f"/ordenes/{id_orden}", json=payload)


def eliminar_orden(id_orden: str) -> dict:
    """Elimina una orden por su ID."""
    return _delete(f"/ordenes/{id_orden}")
