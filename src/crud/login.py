"""
CRUD de login: conexión con los endpoints /usuarios para el logueo.
"""

from src.crud.client import _post


def login(username: str, password: str) -> dict:
    payload = {"username": username, "password": password}
    respuesta = _post("/usuarios/login", json=payload)
    return respuesta
