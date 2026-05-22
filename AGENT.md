# BACKEND AGENT.md

# Proyecto

Sistema de Gestión de Préstamos de Recursos Institucionales para Key Institute.

Backend desarrollado con:

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication

Deployment:

* Railway

---

# Arquitectura Backend

Arquitectura modular basada en capas.

Estructura:

app/
├── main.py
├── config/
├── database/
├── models/
├── schemas/
├── routers/
├── services/
├── repositories/
├── middleware/
├── utils/
├── core/
└── uploads/

---

# Principios

* Código limpio
* Modularidad
* Reutilización
* Separación de responsabilidades
* Validación estricta
* Escalabilidad

---

# Base de Datos

Usar PostgreSQL.

ORM:

* SQLAlchemy

Migraciones:

* Alembic

---

# Entidades Principales

* User
* Resource
* Loan
* LoanDetail
* Return
* Printing3D
* Laboratory

Laboratorios:

* Spark
* KITE
* CLIC
* ACTION LAB

---

# Roles

Roles permitidos:

* admin
* estudiante
* gestor

Permisos:

* admin → acceso total
* gestor → préstamos y devoluciones
* estudiante → operaciones limitadas

---

# Auth

JWT simple.

Guardar:

* access token únicamente

NO refresh tokens.

Token enviado en:
Authorization: Bearer <token>

---

# Seguridad

Validar:

* roles
* permisos
* ownership cuando aplique

Nunca confiar en datos del frontend.

---

# Correos Institucionales

Validar dominio:
@keytest.edu.sv

Usuarios externos no permitidos.

---

# Convenciones de Código

## Idioma

Código completamente en inglés.

## Naming

### Variables

camelCase

### Clases

PascalCase

### Archivos

snake_case o kebab-case consistente

---

# Modelos

Separar:

* SQLAlchemy models
* Pydantic schemas

Nunca exponer modelos directamente.

---

# Schemas

Usar:

* Create schemas
* Update schemas
* Response schemas

Ejemplo:

* UserCreate
* UserUpdate
* UserResponse

---

# Routers

Cada módulo debe tener:

* router
* service
* repository

Ejemplo:
users/

* users_router.py
* users_service.py
* users_repository.py

---

# Repositories

Responsables únicamente de:

* queries
* acceso a DB

NO lógica de negocio.

---

# Services

Responsables de:

* lógica de negocio
* validaciones complejas
* reglas del sistema

---

# Uploads

Guardar imágenes localmente.

Ruta:
uploads/

Guardar en DB:

* únicamente path

Validar:

* tamaño
* extensión
* tipo MIME

---

# Recursos

Campos:

* nombre
* categoría
* código
* stock
* estado
* laboratorio

Estados:

* disponible
* prestado
* mantenimiento
* dañado

---

# Préstamos

Reglas:

* máximo 1 día
* generar código de devolución único
* disminuir stock automáticamente

---

# Devoluciones

Al devolver:

* aumentar stock
* registrar evidencia
* registrar incidencias

Si hay daños:

* incrementar penalizaciones

---

# Impresoras 3D

Registrar:

* código impresora
* tipo material
* gramos
* tiempo estimado
* trabajo individual/grupal

Materiales:

* PLA
* TPU
* ASA

---

# API Conventions

## Versionado

/api/v1/

## Respuestas

Todas las respuestas deben ser consistentes.

Ejemplo:
{
"success": true,
"message": "Loan created successfully",
"data": {}
}

---

# Manejo de Errores

Usar:

* HTTPException
* códigos HTTP correctos

Mensajes claros y consistentes.

---

# Logs

Registrar:

* errores importantes
* auth failures
* uploads
* préstamos críticos

---

# Validaciones

Validar:

* stock disponible
* emails
* permisos
* tipos de archivos
* datos requeridos

Nunca asumir datos válidos.

---

# Performance

Usar:

* relaciones optimizadas
* paginación
* índices en PostgreSQL

Evitar:

* queries innecesarias
* N+1 problems

---

# Deployment

Backend desplegado en:

* Railway

Variables en:
.env

Nunca subir:

* secretos
* tokens
* credenciales

---

# Objetivo Final

Construir un backend:

* seguro
* limpio
* escalable
* mantenible
* profesional
* fácil de extender
