
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
- Usuarios

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
├── src/
│   ├── app.py              # Aplicación FastAPI y manejadores globales
│   ├── core/               # Núcleo: excepciones y respuestas estándar
│   │   ├── exceptions.py   # Excepciones de negocio (NotFound, Conflict, BadRequest…)
│   │   ├── responses.py    # ApiResponse, ApiErrorDetail, success_response, error_response
│   │   └── error_handlers.py # Manejadores que traducen excepciones → JSON estándar
│   ├── database/          # Configuración PostgreSQL y sesión
│   ├── entities/          # Modelos SQLAlchemy (tablas)
│   ├── schemas/            # Modelos Pydantic (validación y serialización)
│   ├── endpoints/          # Rutas FastAPI por recurso
│   ├── crud/               # Cliente HTTP (httpx) que consume la API
│   └── utils/              # Utilidades
│       └── security.py     # Hash de contraseñas (bcrypt)
├── main.py                 # Menú por consola que usa el CRUD contra la API
├── init_db.py              # Crear tablas en la base de datos
├── requirements.txt
├── .github/workflows/ci.yml # Pipeline CI (lint + smoke test)
└── README.md
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
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:

http://localhost:8000

---

# 📖 Documentación de la API

FastAPI genera documentación automática.

### Swagger UI

http://localhost:8000/docs

---

## Video de demostración (examen 2)

Demostración del pipeline en GitHub Actions (rama `dev`) y de migraciones/seeder/esquema en base de datos, según el enunciado del entregable Examen 2

**Ver en YouTube:** [https://youtu.be/63ToPSw8hwM](https://youtu.be/63ToPSw8hwM)

[![Miniatura – demostración](https://img.youtube.com/vi/63ToPSw8hwM/0.jpg)](https://youtu.be/63ToPSw8hwM)

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