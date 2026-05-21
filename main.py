from fastapi import FastAPI
from database import engine, Base
from routers import users, laboratories, resources, prestamos, loan_details, returns, printing_3d, material_3d

# Crear tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Préstamos - Laboratorio")

# Incluir routers
app.include_router(users.router)
app.include_router(laboratories.router)
app.include_router(resources.router)
app.include_router(prestamos.router)
app.include_router(loan_details.router)
app.include_router(returns.router)
app.include_router(printing_3d.router)
app.include_router(material_3d.router)

@app.get("/")
def root():
    return {"message": "API del Sistema de Préstamos funcionando"}