from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config.settings import settings
from app.database.session import SessionLocal
from app.database.seed import seed_laboratories
from app.routers import (
    auth, users, laboratories, resources,
    loans, returns, material_3d, printing_3d,
    reports, uploads, printers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_laboratories(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Sistema de Gestión de Préstamos — Key Institute",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(laboratories.router)
app.include_router(resources.router)
app.include_router(printers.router)
app.include_router(loans.router)
app.include_router(returns.router)
app.include_router(material_3d.router)
app.include_router(printing_3d.router)
app.include_router(reports.router)
app.include_router(uploads.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "gestor-prestamos-recursos"}
