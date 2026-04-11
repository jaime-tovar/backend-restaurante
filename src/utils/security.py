import bcrypt


def hash_password(plain: str) -> str:
    """
    Genera un hash seguro de una contraseña en texto plano utilizando bcrypt.

    La función aplica un salt aleatorio y retorna el hash codificado en UTF-8,
    listo para ser almacenado en base de datos.

    Args:
        plain (str): Contraseña en texto plano.

    Returns:
        str: Contraseña hasheada en formato string.

    Notes:
        - El salt se genera automáticamente en cada ejecución.
        - No es posible recuperar la contraseña original desde el hash.
        - Para validación, usar bcrypt.checkpw().
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash usando bcrypt.

    Compara la contraseña proporcionada con el hash almacenado en base de datos
    utilizando bcrypt.checkpw().

    Args:
        plain (str): Contraseña en texto plano a validar.
        hashed (str): Hash almacenado de la contraseña.

    Returns:
        bool: True si la contraseña coincide con el hash, False en caso contrario.

    Notes:
        - La función no desencripta la contraseña, solo valida coincidencia.
        - El hash debe haber sido generado previamente con bcrypt.
    """
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
