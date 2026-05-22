from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.printer import PrinterResponse

VALID_ESTADOS = {"pendiente", "en_proceso", "completado", "cancelado"}


class Printing3DCreate(BaseModel):
    id_usuario: int
    id_printer: int
    id_material: int
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None


class Printing3DUpdate(BaseModel):
    id_printer: Optional[int] = None
    id_material: Optional[int] = None
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None
    estado: Optional[str] = None


class Printing3DResponse(BaseModel):
    id_impresion: int
    id_usuario: int
    id_printer: int
    id_material: int
    printer: Optional[PrinterResponse] = None
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None
    estado: str
    fecha_solicitud: Optional[datetime] = None

    model_config = {"from_attributes": True}
