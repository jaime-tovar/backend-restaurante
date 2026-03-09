"""
Aplicación FastAPI. Ejecutar con:
  python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import categorias
from src.endpoints import clientes
from src.endpoints import detalle_orden

# Importar modelos para que Base.metadata los conozca
import src.entities.categorias
import src.entities.clientes
import src.entities.detalle_orden


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

app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(detalle_orden.router)


@app.get("/")
def inicio():
    return {"mensaje": "API para restaurante", "docs": "/docs"}
