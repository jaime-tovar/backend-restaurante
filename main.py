"""
Menú por consola que usa el CRUD (cliente de la API Restaurante).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""

import sys
import threading
import time

sys.path.insert(0, ".")
id_usuario_actual = None

from src.crud import (
    listar_usuarios,
    crear_usuario,
    obtener_usuario,
    actualizar_usuario,
    desactivar_usuario,
    login,
)


def _err_conexion(e):
    err = str(e)
    if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
        print(
            "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
        )
    else:
        print(f"  Error: {e}")


def _iniciar_api():
    import uvicorn

    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def menu_login():
    global id_usuario_actual
    while True:
        print("\n--- LOGIN RESTAURANTE ---")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            username = input("Nombre de Usuario: ").strip()
            password = input("Contraseña: ").strip()
            if username and password:
                try:
                    confirmar_login = login(username, password)
                    if confirmar_login.get("success"):
                        print(f"¡Bienvenido!")
                        id_usuario_actual = confirmar_login.get("id_usuario")
                        return True
                    else:
                        print(
                            f"Error inesperado durante el login.\n {confirmar_login.get('message')}"
                        )
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  El nombre de usuario y la contraseña no pueden estar vacíos.")

        elif opcion == "2":
            print(" Por favor crea tu usuario:")
            nombre_completo = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            username = input("Nombre de Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = input("Rol (admin/cliente): ").strip()
            if nombre_completo and email and telefono and username and password and rol:
                try:
                    crear_usuario(
                        nombre_completo, email, telefono, username, password, rol
                    )
                    print("Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
                    return True
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Todos los campos son obligatorios para crear una cuenta.")
        elif opcion == "3":
            print("Saliendo...")
            return False
        else:
            print("Opción no válida. Intenta de nuevo.")


def menu_usuarios() -> None:
    while True:
        print("\n--- MENÚ USUARIOS ---")
        print("1. Listar usuarios")
        print("2. Ver un usuario")
        print("3. Crear usuario")
        print("4. Actualizar usuario")
        print("5. Desactivar usuario")
        print("0. Volver al menú principal")
        opcion = input("Selecciona una opción: ")

        if opcion == "0":
            break
        elif opcion == "1":
            try:
                usuarios = listar_usuarios()
                if not usuarios.get("success"):
                    print("  No hay usuarios.")
                else:
                    for u in usuarios.get("data"):
                        print(
                            f"  ID: {u['id_usuario']} | Nombre: {u['nombre_completo']} | "
                            f"Email: {u['email']} | Teléfono: {u['telefono']} | "
                            f"Username: {u['username']} | Rol: {u['rol']} | "
                            f"Activo: {'Sí' if u['activo'] else 'No'}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif opcion == "2":
            user_id = input("ID del usuario: ").strip()
            if user_id:
                try:
                    usuario = obtener_usuario(user_id)
                    if usuario.get("success"):
                        usuario = usuario.get("data")
                        print(
                            f"  ID: {usuario['id_usuario']} | Nombre: {usuario['nombre_completo']} | "
                            f"Email: {usuario['email']} | Teléfono: {usuario['telefono']} | "
                            f"Username: {usuario['username']} | Rol: {usuario['rol']} | "
                            f"Activo: {'Sí' if usuario['activo'] else 'No'}"
                        )
                    else:
                        print("  Usuario no encontrado.")
                except Exception as e:
                    _err_conexion(e)
        elif opcion == "3":
            print(" LLene los campos para hacer el registro de un nuevo usuario:")
            nombre_completo = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            username = input("Nombre de Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = input("Rol (admin/cliente): ").strip()
            if nombre_completo and email and telefono and username and password and rol:
                try:
                    crear_usuario(
                        nombre_completo, email, telefono, username, password, rol
                    )
                    print("Usuario creado exitosamente.")
                    return True
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Todos los campos son obligatorios para crear un usuario.")
        elif opcion == "4":
            id_user = input("ID del usuario a actualizar: ").strip()
            if not id_user:
                continue
            print("Si dejas el campo vacío, entonces ese atributo no cambiará")
            nombre_completo = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            username = input("Nombre de Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = input("Rol (admin/cliente): ").strip()
            kwargs = {}
            if nombre_completo:
                kwargs["nombre_completo"] = nombre_completo
            if email:
                kwargs["email"] = email
            if telefono:
                kwargs["telefono"] = telefono
            if username:
                kwargs["username"] = username
            if password:
                kwargs["password"] = password
            if rol:
                kwargs["rol"] = rol
            try:
                actualizar_usuario(id_user, **kwargs)
                print(" Usuario actualizado existosamente.")
            except Exception as e:
                _err_conexion(e)
        elif opcion == "5":
            id_user = input("ID usuario a desactivar/eliminar: ").strip()
            if id_user:
                try:
                    kwargs = {"activo": False}
                    desactivar_usuario(id_user, **kwargs)
                    print(" Usuario desactivado/eliminado.")
                except Exception as e:
                    _err_conexion(e)
        else:
            print("Opción no válida. Intenta de nuevo.")


def main():
    print("API Restaurante - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_iniciar_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")

    if not menu_login():
        print("No se inició sesión")
        return
    while True:
        print("\n========== MÓDULOS RESTAURANTE ==========")
        print(
            "1. Usuarios  2. Categorias  3. Clientes 4. Detalles de Orden  "
            "5. Facturas 6. Mesas 7. Métodos de Pago  8. Ordenes  9. Platos  "
            "10. Reservaciones  0. Salir",
        )
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
            menu_usuarios()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
