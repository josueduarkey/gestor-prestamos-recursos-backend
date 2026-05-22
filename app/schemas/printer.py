from pydantic import BaseModel
from typing import Optional

VALID_ESTADOS = {"disponible", "en_uso", "mantenimiento"}


class PrinterCreate(BaseModel):
    codigo: str
    nombre: Optional[str] = None
    estado: str = "disponible"
    id_laboratorio: int


class PrinterUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    estado: Optional[str] = None
    id_laboratorio: Optional[int] = None


class PrinterResponse(BaseModel):
    id_printer: int
    codigo: str
    nombre: Optional[str] = None
    estado: str
    id_laboratorio: Optional[int] = None

    model_config = {"from_attributes": True}
