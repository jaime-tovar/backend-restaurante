"""
CRUD de factura: conexión con los endpoints /facturas.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_facturas():
    """
    Listar todas las facturas.
    """
    return _get("/facturas")


def obtener_factura(factura_id: str) -> dict:
    """
    Obtener una factura por su ID.
    """
    return _get(f"/facturas/{factura_id}")


def crear_factura(
    orden_id: str,
    subtotal: float,
    descuento: float,
    total: float,
    metodo_pago_id: str,
) -> dict:
    """
    Crear una nueva factura.
    """
    payload = {
        "id_orden": orden_id,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
        "id_metodo_pago": metodo_pago_id,
    }
    return _post("/facturas", json=payload)


def actualizar_factura(
    factura_id: str,
    subtotal: float | None = None,
    descuento: float | None = None,
    total: float | None = None,
    metodo_pago_id: str | None = None,
) -> dict:
    """
    Actualizar una factura existente.
    """
    payload = {}
    if subtotal is not None:
        payload["subtotal"] = subtotal
    if descuento is not None:
        payload["descuento"] = descuento
    if total is not None:
        payload["total"] = total
    if metodo_pago_id is not None:
        payload["id_metodo_pago"] = metodo_pago_id
    return _put(f"/facturas/{factura_id}", json=payload)


def eliminar_factura(factura_id: str) -> dict:
    """
    Eliminar una factura por su ID.
    """
    return _delete(f"/facturas/{factura_id}")
