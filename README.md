# Gestor de Préstamos de Recursos — Key Institute

Backend para la gestión de préstamos de recursos en los laboratorios de Key Institute.

**Stack:** FastAPI · PostgreSQL · SQLAlchemy · Alembic · Docker

---

## Requisitos

| Herramienta | Versión mínima |
|-------------|----------------|
| Docker      | 24+            |
| Docker Compose | v2 (`docker compose`) |
| Python      | 3.11+ (solo si corres la app localmente) |

---

## Opción A — Todo en Docker (recomendado)

La forma más rápida. No necesitas Python instalado.

### 1. Clona el repositorio

```bash
git clone <url-del-repo>
cd gestor-prestamos-recursos-backend
```

### 2. Crea el archivo `.env`

En la terminal (bash/zsh):
```bash
cp .env.example .env
```
En Windows (PowerShell):
```powershell
copy .env.example .env
```

Edita `.env` y cambia al menos `SECRET_KEY`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/prestamos_keylab
POSTGRES_DB=prestamos_keylab
POSTGRES_USER=user
POSTGRES_PASSWORD=password
SECRET_KEY=cambia-esto-por-una-clave-secreta-larga
```

### 3. Levanta todo

Asegúrate de tener **Docker Desktop** iniciado.

```bash
docker compose up --build
```

Esto:
1. Levanta PostgreSQL y espera a que esté listo
2. Corre las migraciones automáticamente (`alembic upgrade head`)
3. Inserta los 4 laboratorios por defecto (Spark, KITE, CLIC, ACTION LAB)
4. Inicia el servidor FastAPI en el puerto `8000`

### URLs disponibles

| Servicio     | URL                              |
|--------------|----------------------------------|
| API          | http://localhost:8000            |
| Swagger Docs | http://localhost:8000/api/docs   |
| ReDoc        | http://localhost:8000/api/redoc  |
| pgAdmin      | http://localhost:5050            |

### Detener

```bash
docker compose down
```

Para también borrar los datos de la base de datos:

```bash
docker compose down -v
```

---

## Opción B — Base de datos en Docker, app local

Útil para desarrollo activo con hot-reload.

### 1. Clona y configura `.env`

```bash
git clone <url-del-repo>
cd gestor-prestamos-recursos-backend
cp .env.example .env
```

### 2. Levanta solo la base de datos

```bash
docker compose up postgres pgadmin -d
```

### 3. Crea el entorno virtual e instala dependencias

```bash
python -m venv .venv
```

Activa el entorno:
- **Mac/Linux:** `source .venv/bin/activate`
- **Windows (CMD):** `.venv\Scripts\activate`
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`

Luego instala las librerías:
```bash
pip install -r requirements.txt
```

### 4. Corre las migraciones

Solo la primera vez (o cuando haya cambios en los modelos):

```bash
alembic upgrade head
```

### 5. Inicia el servidor

```bash
uvicorn app.main:app --reload
```

### URLs disponibles

| Servicio     | URL                              |
|--------------|----------------------------------|
| API          | http://localhost:8000            |
| Swagger Docs | http://localhost:8000/api/docs   |
| ReDoc        | http://localhost:8000/api/redoc  |
| pgAdmin      | http://localhost:5050            |

---

## Migraciones con Alembic

### Generar una migración (cuando cambias un modelo)

```bash
# Con la DB corriendo:
alembic revision --autogenerate -m "descripcion del cambio"
```

### Aplicar migraciones pendientes

```bash
alembic upgrade head
```

### Ver el estado actual

```bash
alembic current
```

### Revertir la última migración

```bash
alembic downgrade -1
```

> **Importante:** El archivo generado en `migrations/versions/` debe subirse al repositorio. Nunca lo elimines manualmente.

---

## Variables de entorno

| Variable                    | Descripción                              | Requerida |
|-----------------------------|------------------------------------------|-----------|
| `DATABASE_URL`              | URL de conexión a PostgreSQL             | Sí        |
| `SECRET_KEY`                | Clave para firmar JWT (larga y aleatoria)| Sí        |
| `ALGORITHM`                 | Algoritmo JWT (default: `HS256`)         | No        |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token (default: `60`)   | No        |
| `POSTGRES_DB`               | Nombre de la base de datos (Docker)      | No        |
| `POSTGRES_USER`             | Usuario de PostgreSQL (Docker)           | No        |
| `POSTGRES_PASSWORD`         | Contraseña de PostgreSQL (Docker)        | No        |
| `POSTGRES_PORT`             | Puerto local de PostgreSQL (default: `5432`) | No   |
| `PGADMIN_DEFAULT_EMAIL`     | Email de acceso a pgAdmin                | No        |
| `PGADMIN_DEFAULT_PASSWORD`  | Contraseña de pgAdmin                    | No        |
| `PGADMIN_PORT`              | Puerto de pgAdmin (default: `5050`)      | No        |

---

## Estructura del proyecto

```
app/
├── main.py              # Entry point FastAPI
├── config/
│   └── settings.py      # Variables de entorno (Pydantic Settings)
├── database/
│   ├── session.py       # Engine + SessionLocal + Base
│   └── seed.py          # Laboratorios por defecto
├── core/
│   ├── security.py      # JWT + bcrypt
│   └── dependencies.py  # get_db, get_current_user, require_roles
├── models/              # Modelos SQLAlchemy (uno por entidad)
├── schemas/             # Schemas Pydantic Create/Update/Response
├── repositories/        # Acceso a DB — solo queries, sin lógica
├── services/            # Lógica de negocio y validaciones
├── routers/             # Endpoints HTTP (thin layer)
└── utils/
    └── validators.py    # Validaciones reutilizables
migrations/              # Alembic migrations
uploads/                 # Archivos subidos
```

---

## Endpoints principales

### Auth
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Login — retorna JWT |

### Usuarios
| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| POST | `/api/v1/users/register` | Público | Registro de estudiantes |
| POST | `/api/v1/users/staff` | Admin | Crear gestor o admin |
| GET | `/api/v1/users/me` | Autenticado | Perfil propio |
| GET | `/api/v1/users/` | Admin/Gestor | Listar usuarios |
| PUT | `/api/v1/users/{carnet}` | Admin | Editar usuario |
| POST | `/api/v1/users/{carnet}/reset-penalties` | Admin | Resetear penalizaciones |

### Laboratorios
| Método | Ruta | Acceso |
|--------|------|--------|
| GET | `/api/v1/laboratories/` | Público |
| POST | `/api/v1/laboratories/` | Admin |
| PUT | `/api/v1/laboratories/{id}` | Admin |

### Recursos (Herramientas)
| Método | Ruta | Acceso |
|--------|------|--------|
| GET | `/api/v1/resources/` | Autenticado |
| POST | `/api/v1/resources/` | Admin/Gestor |
| PUT | `/api/v1/resources/{id}` | Admin/Gestor |
| DELETE | `/api/v1/resources/{id}` | Admin |

Filtros disponibles: `?categoria=X&id_laboratorio=1&estado=disponible`

### Préstamos
| Método | Ruta | Acceso |
|--------|------|--------|
| GET | `/api/v1/loans/` | Admin/Gestor |
| POST | `/api/v1/loans/` | Admin/Gestor |
| PATCH | `/api/v1/loans/{id}/close` | Admin/Gestor |

Filtros: `?id_usuario=X&estado=activo&overdue_only=true`

### Devoluciones
| Método | Ruta | Acceso |
|--------|------|--------|
| POST | `/api/v1/returns/` | Admin/Gestor |
| GET | `/api/v1/returns/` | Admin/Gestor |

### Impresoras 3D
| Método | Ruta | Acceso |
|--------|------|--------|
| GET | `/api/v1/printings-3d/` | Admin/Gestor |
| POST | `/api/v1/printings-3d/` | Admin/Gestor |

Filtros: `?codigo_impresora=IMP-01&id_material=1`

---

## Reglas de negocio

- Solo se permiten correos `@keytest.edu.sv`
- Los préstamos tienen un límite de **1 día**
- Un usuario **no puede pedir prestado** si:
  - Tiene un préstamo activo vencido (pasó `fecha_limite`)
  - Tiene 3 o más penalizaciones
- Las penalizaciones aumentan cuando:
  - Devuelve con retraso (+1)
  - Devuelve con daños (`hay_danios = true`) (+1)
- Al devolver, el stock del recurso se restaura automáticamente

---

## Deploy en Railway

1. Conecta el repositorio en Railway
2. Agrega un plugin de **PostgreSQL** — Railway inyecta `DATABASE_URL` automáticamente
3. Configura las variables de entorno: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
4. Railway usa el `railway.toml` para correr las migraciones antes de iniciar el servidor

```toml
# railway.toml (ya incluido en el repo)
[deploy]
startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```
