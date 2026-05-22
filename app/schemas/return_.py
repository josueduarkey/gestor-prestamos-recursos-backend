from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReturnCreate(BaseModel):
    id_loan: int
    evidencia: Optional[str] = None
    descripcion: Optional[str] = None
    hay_danios: bool = False


class ReturnUpdate(BaseModel):
    evidencia: Optional[str] = None
    descripcion: Optional[str] = None
    hay_danios: Optional[bool] = None
    estado: Optional[str] = None


class ReturnResponse(BaseModel):
    id_devolucion: int
    id_loan: int
    fecha_devolucion: Optional[datetime] = None
    estado: str
    evidencia: Optional[str] = None
    descripcion: Optional[str] = None
    hay_danios: bool

    model_config = {"from_attributes": True}
