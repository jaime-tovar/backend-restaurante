"""
CRUD de cliente: conexión con los endpoints /clientes.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_clientes():
    """
    Listar todos los clientes.
    """
    return _get("/clientes")


def obtener_cliente(cliente_id: str) -> dict:
    """
    Obtener un cliente por su ID.
    """
    return _get(f"/clientes/{cliente_id}")


def crear_cliente(
    nombre: str, apellido: str, email: str, telefono: str, activo: bool = True
) -> dict:
    """
    Crear un nuevo cliente.
    """
    payload = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono,
        "activo": activo,
    }
    return _post("/clientes", json=payload)


def actualizar_cliente(
    cliente_id: str,
    nombre: str | None = None,
    apellido: str | None = None,
    email: str | None = None,
    telefono: str | None = None,
    activo: bool | None = None,
) -> dict:
    """
    Actualizar un cliente existente.
    """
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if apellido is not None:
        payload["apellido"] = apellido
    if email is not None:
        payload["email"] = email
    if telefono is not None:
        payload["telefono"] = telefono
    if activo is not None:
        payload["activo"] = activo
    return _put(f"/clientes/{cliente_id}", json=payload)


def eliminar_cliente(cliente_id: str) -> dict:
    """
    Eliminar un cliente por su ID.
    """
    return _delete(f"/clientes/{cliente_id}")
