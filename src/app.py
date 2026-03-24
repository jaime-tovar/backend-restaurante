"""
Aplicación FastAPI. Ejecutar con:
  python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import (
    categorias,
    clientes,
    detalles_orden,
    metodos_pago,
    ordenes,
    platos,
    facturas,
    mesas,
    reservaciones,
    usuarios,
)

# Importar modelos para que Base.metadata los conozca
import src.entities.categoria
import src.entities.cliente
import src.entities.detalle_orden
import src.entities.orden
import src.entities.plato
import src.entities.factura
import src.entities.mesa
import src.entities.metodo_pago
import src.entities.reservacion
import src.entities.usuario


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    # shutdown si hiciera falta


app = FastAPI(
    title="API Restaurante",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(detalles_orden.router)
app.include_router(ordenes.router)
app.include_router(platos.router)
app.include_router(facturas.router)
app.include_router(mesas.router)
app.include_router(metodos_pago.router)
app.include_router(reservaciones.router)


@app.get("/")
def inicio():
    return {"mensaje": "API para restaurante", "docs": "/docs"}
