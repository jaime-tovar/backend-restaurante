"""
Aplicación FastAPI. Ejecutar con:
  python -m uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.responses import success_response
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
    login,
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
    description="API con FastAPI, SQLAlchemy y PostgreSQL - CRUD completo para un sistema de restaurante",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Manejadores globales de excepciones (estructura de respuesta unificada)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(login.router)
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
    return success_response(data={"mensaje": "API para restaurante", "docs": "/docs"})
