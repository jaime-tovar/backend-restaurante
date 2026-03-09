"""
CRUD de detalle de orden: conexión con los endpoints /detalle_orden
"""

from src.crud.client import _delete, _get, _post, _put


def listar_detalles_orden():
    """
    Listar todos los detalles de orden.
    """
    return _get("/detalle_orden")


def obtener_detalle_orden(detalle_id: str) -> dict:
    """
    Obtener un detalle de orden por su ID.
    """
    return _get(f"/detalle_orden/{detalle_id}")


def crear_detalle_orden(
    id_orden: str, id_plato: str, cantidad: int, precio_unitario: float
) -> dict:
    """
    Crear un nuevo detalle de orden.
    """
    payload = {
        "id_orden": id_orden,
        "id_plato": id_plato,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
    }
    return _post("/detalle_orden", json=payload)


def actualizar_detalle_orden(
    detalle_id: str,
    id_orden: str | None = None,
    id_plato: str | None = None,
    cantidad: int | None = None,
    precio_unitario: float | None = None,
) -> dict:
    """
    Actualizar un detalle de orden existente.
    """
    payload = {}
    if id_orden is not None:
        payload["id_orden"] = id_orden
    if id_plato is not None:
        payload["id_plato"] = id_plato
    if cantidad is not None:
        payload["cantidad"] = cantidad
    if precio_unitario is not None:
        payload["precio_unitario"] = precio_unitario
    return _put(f"/detalle_orden/{detalle_id}", json=payload)


def eliminar_detalle_orden(detalle_id: str) -> dict:
    """
    Eliminar un detalle de orden por su ID.
    """
    return _delete(f"/detalle_orden/{detalle_id}")
