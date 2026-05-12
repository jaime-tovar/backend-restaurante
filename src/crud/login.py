"""
CRUD de login: conexión con los endpoints /usuarios para el logueo.
"""

from src.crud.client import _post, set_auth_token


def login(username: str, password: str) -> dict:
    payload = {"username": username, "password": password}
    respuesta = _post("/usuarios/login", json=payload)
    token = respuesta.get("access_token")
    if token:
        set_auth_token(token)
    return respuesta
