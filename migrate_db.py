"""
Script para crear y actualizar el esquema de la BD.
- Crea las tablas definidas en los modelos (create_all).
- Ejecuta migraciones SQL en migrations/ en orden (para alteraciones futuras).

Uso:
  python migrate_db.py

Requiere DATABASE_URL en .env (o entorno). Seguro para ejecutar varias veces.
"""

import os
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

import src.entities.usuario
import src.entities.categoria
import src.entities.cliente
import src.entities.detalle_orden
import src.entities.factura
import src.entities.mesa
import src.entities.metodo_pago
import src.entities.orden
import src.entities.plato
import src.entities.reservacion

from src.database.config import engine, create_tables

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def ensure_migrations_table(conn):
    conn.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS _schema_migrations (
            name VARCHAR(255) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
        )
    )
    conn.commit()


def applied_migrations(conn):
    result = conn.execute(text("SELECT name FROM _schema_migrations"))
    return {row[0] for row in result}


def run_sql_file(conn, path: Path):
    sql = path.read_text(encoding="utf-8")

    conn.execute(text(sql))  # ejecutar todo el archivo SQL de una vez
    conn.commit()


def run_pending_migrations(conn):
    if not MIGRATIONS_DIR.exists():
        return

    applied = applied_migrations(conn)
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    for f in files:
        if f.name in applied:
            continue

        print(f"Aplicando migración: {f.name}")
        run_sql_file(conn, f)

        conn.execute(
            text("INSERT INTO _schema_migrations (name) VALUES (:name)"),
            {"name": f.name},
        )
        conn.commit()


def main():
    try:
        print("Creando tablas...")
        create_tables()

        with engine.connect() as conn:
            ensure_migrations_table(conn)
            print("Ejecutando migraciones...")
            run_pending_migrations(conn)

        print(" Base de datos actualizada correctamente")

    except OperationalError as e:
        print(" Error de conexión:", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
