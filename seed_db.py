"""
Seeder: datos iniciales para dev/QA/prod.
Idempotente: no duplica registros si ya existen (por codigo o identificador).

Uso:
  python seed_db.py

Requiere DATABASE_URL. Ejecutar después de migrate_db.py.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.entities.categoria import Categoria
from src.entities.cliente import Cliente
from src.entities.mesa import Mesa
from src.entities.metodo_pago import MetodoPago
from src.entities.plato import Plato
from src.entities.usuario import Usuario
from src.utils.security import hash_password

USUARIO_INICIAL = {
    "nombre_completo": "Administrador Genérico",
    "username": "admin",
    "email": "admin@restaurante.local",
    "telefono": "3001234567",
    "password": "Admin123!",
    "rol": "admin",
    "activo": True,
}

CATEGORIAS_INICIALES = [
    {"descripcion": "Bebidas", "activo": True},
    {"descripcion": "Platos Fuertes", "activo": True},
    {"descripcion": "Postres", "activo": True},
]

CLIENTES_INICIALES = [
    {
        "documento": "222222222222",
        "nombre": "Consumidor Final",
        "apellido": "",
        "email": "consumidor.final@test.com",
        "telefono": "222222222222",
        "activo": True,
    }
]

PLATOS_INICIALES = [
    {
        "nombre": "Limonada Cerezada",
        "descripcion": "Jugo a base de limón con esencia de cereza",
        "precio": 5000.00,
        "categoria": "Bebidas",
        "activo": True,
    },
    {
        "nombre": "Cordon Bleu",
        "descripcion": "Rollo de pollo con jamón y queso",
        "precio": 18000.00,
        "categoria": "Platos Fuertes",
        "activo": True,
    },
]

MESAS_INICIALES = [
    {"numero_mesa": 1, "capacidad": 4, "estado": "disponible"},
    {"numero_mesa": 2, "capacidad": 2, "estado": "disponible"},
]

METODOS_PAGO_INICIALES = [
    {"nombre": "Efectivo", "activo": True},
    {"nombre": "Tarjeta Débito", "activo": True},
    {"nombre": "Tarjeta Crédito", "activo": True},
    {"nombre": "Transferencia/QR", "activo": True},
]


def get_or_create_admin(db) -> Usuario:
    """Crea el usuario admin si no existe y devuelve su instancia (para id_usuario_creacion)."""
    admin = (
        db.query(Usuario)
        .filter(Usuario.username == USUARIO_INICIAL["username"])
        .first()
    )
    if admin:
        return admin
    u = USUARIO_INICIAL.copy()
    u["password"] = hash_password(u.pop("password"))
    admin = Usuario(**u)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("  Usuario creado: admin")
    return admin


def seed_categorias(db, admin):

    for cat in CATEGORIAS_INICIALES:
        existe = db.query(Categoria).filter_by(descripcion=cat["descripcion"]).first()

        if not existe:
            nueva_categoria = Categoria(
                descripcion=cat["descripcion"],
                activo=cat["activo"],
                id_usuario_creacion=admin.id_usuario,
            )
            db.add(nueva_categoria)
            print(f" Categoría '{cat['descripcion']}' creada")
        else:
            print(f" Categoría '{cat['descripcion']}' ya existe")


def seed_platos(db, admin):

    for plato in PLATOS_INICIALES:
        # Buscar categoría por nombre
        categoria = (
            db.query(Categoria).filter_by(descripcion=plato["categoria"]).first()
        )

        if not categoria:
            print(f" No existe categoría {plato['categoria']}")
            continue

        # Validación idempotente (nombre + categoría)
        existe = (
            db.query(Plato)
            .filter_by(nombre=plato["nombre"], id_categoria=categoria.id_categoria)
            .first()
        )

        if not existe:
            nuevo_plato = Plato(
                nombre=plato["nombre"],
                descripcion=plato["descripcion"],
                precio=plato["precio"],
                activo=plato["activo"],
                id_categoria=categoria.id_categoria,
                id_usuario_creacion=admin.id_usuario,
            )
            db.add(nuevo_plato)
            print(f" Plato '{plato['nombre']}' creado")
        else:
            print(f" Plato '{plato['nombre']}' ya existe")


def seed_clientes(db, admin):

    for cliente in CLIENTES_INICIALES:
        # Puedes validar por documento (mejor opción)
        existe = db.query(Cliente).filter_by(documento=cliente["documento"]).first()

        if not existe:
            nuevo_cliente = Cliente(
                documento=cliente["documento"],
                nombre=cliente["nombre"],
                apellido=cliente["apellido"],
                email=cliente["email"],
                telefono=cliente["telefono"],
                activo=cliente["activo"],
                id_usuario_creacion=admin.id_usuario,
            )
            db.add(nuevo_cliente)
            print(f" Cliente {cliente['nombre']} creado")
        else:
            print(f" Cliente {cliente['documento']} ya existe")


def seed_mesas(db, admin):

    for mesa in MESAS_INICIALES:
        existe = db.query(Mesa).filter_by(numero_mesa=mesa["numero_mesa"]).first()

        if not existe:
            nueva_mesa = Mesa(
                numero_mesa=mesa["numero_mesa"],
                capacidad=mesa["capacidad"],
                estado=mesa["estado"],
                id_usuario_creacion=admin.id_usuario,
            )
            db.add(nueva_mesa)
            print(f" Mesa {mesa['numero_mesa']} creada")
        else:
            print(f" Mesa {mesa['numero_mesa']} ya existe")


def seed_metodos_pago(db, admin):

    for metodo in METODOS_PAGO_INICIALES:
        existe = db.query(MetodoPago).filter_by(nombre=metodo["nombre"]).first()

        if not existe:
            nuevo_metodo = MetodoPago(
                nombre=metodo["nombre"],
                activo=metodo["activo"],
                id_usuario_creacion=admin.id_usuario,
            )
            db.add(nuevo_metodo)
            print(f" Método de pago '{metodo['nombre']}' creado")
        else:
            print(f" Método de pago '{metodo['nombre']}' ya existe")


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando usuario admin (si no existe)...")
            admin = get_or_create_admin(db)

            print("Sembrando categorías para platos...")
            seed_categorias(db, admin)
            print("Sembrando platos...")
            seed_platos(db, admin)
            print("Sembrando consumidor final como cliente...")
            seed_clientes(db, admin)
            print("Sembrado mesas...")
            seed_mesas(db, admin)
            print("Sembrando métodos de pago...")
            seed_metodos_pago(db, admin)
            db.commit()
            print("Seed completado.")
        finally:
            db.close()
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
