from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    carnet: int
    nombre: str
    correo: EmailStr
    password: str
    generacion: str
    role: str = "estudiante"


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = None
    generacion: Optional[str] = None
    role: Optional[str] = None


class ApplyPenaltyRequest(BaseModel):
    cantidad: int = 1
    motivo: Optional[str] = None


class UserResponse(BaseModel):
    carnet: int
    nombre: str
    correo: str
    estado: Optional[str] = None
    penalizaciones: int = 0
    generacion: str
    role: str

    model_config = {"from_attributes": True}
