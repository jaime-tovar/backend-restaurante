
# API REST con FastAPI – Sistema de Gestión de Restaurante

Proyecto desarrollado para el curso **Aplicaciones y Servicios Web**.  
La aplicación expone una **API REST** construida con **FastAPI**, ejecutada con **Uvicorn** y conectada a una base de datos **PostgreSQL en Neon**.

---

# 📌 Objetivo del Proyecto

Desarrollar una aplicación backend que permita gestionar diferentes procesos de un sistema de restaurante mediante una **API RESTful**, implementando buenas prácticas de desarrollo backend, manejo de base de datos y arquitectura modular.

La API permite administrar entidades como:

- Clientes
- Mesas
- Categorías de platos
- Platos
- Órdenes
- Detalle de órdenes
- Facturas
- Métodos de pago
- Reservaciones

---

# 🛠 Tecnologías Utilizadas

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- Neon (PostgreSQL Serverless)
- SQLAlchemy
- Pydantic

---

# 📁 Estructura del Proyecto

```
.
│   .env
│   .gitignore
│   init_db.py
│   README.md
│   requirements.txt
│
└── src
    │   app.py
    │   __init__.py
    │
    ├── crud
    │       categoria.py
    │       client.py
    │       cliente.py
    │       detalle_orden.py
    │       factura.py
    │       mesa.py
    │       metodo_pago.py
    │       orden.py
    │       plato.py
    │       reservacion.py
    │
    ├── database
    │       config.py
    │       __init__.py
    │
    ├── endpoints
    │       categorias.py
    │       clientes.py
    │       detalle_orden.py
    │       facturas.py
    │       mesas.py
    │       metodo_pago.py
    │       orden.py
    │       platos.py
    │       reservaciones.py
    │       __init__.py
    │
    ├── entities
    │       categorias.py
    │       clientes.py
    │       detalle_orden.py
    │       facturas.py
    │       mesas.py
    │       metodos_pago.py
    │       ordenes.py
    │       platos.py
    │       reservaciones.py
    │       __init__.py
    │
    └── schemas
            categoria_schema.py
            cliente_schema.py
            detalle_orden_schema.py
            factura_schema.py
            mesa_schema.py
            metodo_pago_schema.py
            orden_schema.py
            plato_schema.py
            reservacion_schema.py
            __init__.py
```

---

# 📂 Descripción de Carpetas

| Carpeta | Descripción |
|--------|-------------|
| src/app.py | Punto de entrada de la aplicación FastAPI |
| crud | Contiene la lógica de acceso a datos (Create, Read, Update, Delete) |
| database | Configuración de conexión a la base de datos |
| endpoints | Define las rutas y endpoints de la API |
| entities | Modelos de base de datos utilizando SQLAlchemy |
| schemas | Esquemas de validación y serialización usando Pydantic |

---

# ⚙️ Instalación del Proyecto

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/jaime-tovar/backend-restaurante
cd backend-restaurante
```

---

## 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```
DATABASE_URL=postgresql://usuario:password@host/database
```

Esta variable se utiliza para establecer la conexión con la base de datos **PostgreSQL en Neon**.

---

# 🗄 Inicializar Base de Datos

Ejecutar:

```bash
python init_db.py
```

Este script crea las tablas necesarias en la base de datos.

---

# 🚀 Ejecutar la Aplicación

Para iniciar el servidor:

```bash
uvicorn src.app:app --reload
```

La API estará disponible en:

http://localhost:8000

---

# 📖 Documentación de la API

FastAPI genera documentación automática.

### Swagger UI

http://localhost:8000/docs

---

# 📚 Conceptos Aplicados

Durante el desarrollo del proyecto se aplicaron conceptos como:

- Arquitectura modular para APIs
- Separación de responsabilidades
- Uso de ORM para acceso a datos
- Validación de datos con Pydantic
- Desarrollo de APIs RESTful
- Conexión a bases de datos en la nube

---

# 👨‍💻 Autor

Proyecto desarrollado para el curso:

**Aplicaciones y Servicios Web**  
Programa de **Tecnología en Desarrollo de Software**