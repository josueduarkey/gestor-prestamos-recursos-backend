from pydantic import BaseModel
from typing import Optional, List
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


class LoanResourceItem(BaseModel):
    id_recurso: int
    nombre: str
    codigo: Optional[str] = None
    cantidad: int


class ReturnSummary(BaseModel):
    id_devolucion: int
    fecha_devolucion: Optional[datetime] = None
    hay_danios: bool
    descripcion: Optional[str] = None


class LoanDetailedResponse(LoanResponse):
    is_overdue: bool = False
    resources: List[LoanResourceItem] = []
    return_info: Optional[ReturnSummary] = None
