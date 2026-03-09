"""
CRUD de plato: conexión con los endpoints /platos.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_platos():
    """Obtiene la lista de platos."""
    return _get("/platos")


def obtener_plato(id_plato):
    """Obtiene un plato por su ID."""
    return _get(f"/platos/{id_plato}")


def crear_plato(
    id_categoria: str, nombre: str, descripcion: str, precio: float, activo: bool = True
) -> dict:
    """Crea un nuevo plato."""
    payload = {
        "id_categoria": id_categoria,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "activo": activo,
    }
    return _post("/platos", json=payload)


def actualizar_plato(
    id_plato: str,
    id_categoria: str,
    nombre: str,
    descripcion: str,
    precio: float,
    activo: bool = True,
) -> dict:
    """Actualiza un plato existente."""
    payload = {
        "id_categoria": id_categoria,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "activo": activo,
    }
    return _put(f"/platos/{id_plato}", json=payload)


def eliminar_plato(id_plato: str) -> dict:
    """Elimina un plato por su ID."""
    return _delete(f"/platos/{id_plato}")
