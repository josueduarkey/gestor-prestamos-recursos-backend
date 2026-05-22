from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoanCreate(BaseModel):
    id_usuario: int
    responsabilidad: bool


class LoanUpdate(BaseModel):
    estado: Optional[str] = None
    responsabilidad: Optional[bool] = None


class LoanResponse(BaseModel):
    id_loan: int
    id_usuario: int
    codigo_devolucion: str
    responsabilidad: bool
    estado: str
    fecha_prestamo: Optional[datetime] = None
    fecha_limite: Optional[datetime] = None

    model_config = {"from_attributes": True}
