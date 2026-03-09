"""
CRUD de método de pago: conexión con los endpoints /metodos_pago.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_metodos_pago():
    """Obtiene la lista de métodos de pago."""
    return _get("/metodos_pago")


def obtener_metodo_pago(id_metodo_pago):
    """Obtiene un método de pago por su ID."""
    return _get(f"/metodos_pago/{id_metodo_pago}")


def crear_metodo_pago(nombre: str, activo: bool = True) -> dict:
    """Crea un nuevo método de pago."""
    payload = {"nombre": nombre, "activo": activo}
    return _post("/metodos_pago", json=payload)


def actualizar_metodo_pago(id_metodo_pago, nombre: str, activo: bool) -> dict:
    """Actualiza un método de pago existente."""
    payload = {"nombre": nombre, "activo": activo}
    return _put(f"/metodos_pago/{id_metodo_pago}", json=payload)


def eliminar_metodo_pago(id_metodo_pago) -> dict:
    """Elimina un método de pago por su ID."""
    return _delete(f"/metodos_pago/{id_metodo_pago}")
