"""
CRUD de usuario: conexión con los endpoints /usuarios.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_usuarios() -> list:
    """
    Listar todos los usuarios.
    """
    return _get("/usuarios")


def obtener_usuario(usuario_id: str) -> dict:
    """
    Obtener un usuario por su ID.
    """
    return _get(f"/usuarios/{usuario_id}")


def crear_usuario(
    nombre_completo: str,
    email: str,
    telefono: str,
    username: str,
    password: str,
    rol: str,
    activo: bool = True,
) -> dict:
    payload = {
        "nombre_completo": nombre_completo,
        "email": email,
        "telefono": telefono,
        "username": username,
        "activo": activo,
        "password": password,
        "rol": rol,
    }
    return _post("/usuarios", json=payload)


def actualizar_usuario(
    usuario_id: str,
    nombre_completo: str | None = None,
    email: str | None = None,
    telefono: str | None = None,
    username: str | None = None,
    password: str | None = None,
    rol: str | None = None,
    activo: bool | None = None,
) -> dict:
    payload = {
        "nombre_completo": nombre_completo,
        "email": email,
        "telefono": telefono,
        "username": username,
        "password": password,
        "rol": rol,
        "activo": activo,
    }
    # Eliminar claves con valor None para no actualizar esos campos
    payload = {k: v for k, v in payload.items() if v is not None}
    return _put(f"/usuarios/{usuario_id}", json=payload)


def desactivar_usuario(usuario_id: str, activo: bool = False) -> None:
    """
    Desactivar un usuario (establecer activo=False).
    """
    payload = {"activo": activo}
    return _put(f"/usuarios/{usuario_id}", json=payload)
