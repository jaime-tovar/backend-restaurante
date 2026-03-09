"""
CRUD de categoría: conexión con los endpoints /categorias.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_categorias():
    """
    Listar todas las categorías.
    """
    return _get("/categorias")


def obtener_categoria(categoria_id: str) -> dict:
    """
    Obtener una categoría por su ID.
    """
    return _get(f"/categorias/{categoria_id}")


def crear_categoria(nombre: str, activo: bool = True) -> dict:
    """
    Crear una nueva categoría.
    """
    payload = {"nombre": nombre, "activo": activo}
    return _post("/categorias", json=payload)


def actualizar_categoria(categoria_id: str, nombre: str, activo: bool) -> dict:
    """
    Actualizar una categoría existente.
    """
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if activo is not None:
        payload["activo"] = activo
    return _put(f"/categorias/{categoria_id}", json=payload)


def eliminar_categoria(categoria_id: str) -> dict:
    """
    Eliminar una categoría por su ID.
    """
    return _delete(f"/categorias/{categoria_id}")
