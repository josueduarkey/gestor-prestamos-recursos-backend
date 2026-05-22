from pydantic import BaseModel
from typing import Optional


class Printing3DCreate(BaseModel):
    id_loan: int
    id_material: int
    codigo_impresora: str
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None


class Printing3DUpdate(BaseModel):
    codigo_impresora: Optional[str] = None
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None


class Printing3DResponse(BaseModel):
    id_impresion: int
    id_loan: int
    id_material: int
    codigo_impresora: str
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None

    model_config = {"from_attributes": True}
