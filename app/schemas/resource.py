from pydantic import BaseModel
from typing import Optional

VALID_ESTADOS = {"disponible", "prestado", "mantenimiento", "dañado"}


class ResourceCreate(BaseModel):
    nombre: str
    categoria: Optional[str] = None
    codigo: Optional[str] = None
    cantidad_total: int
    cantidad_disponible: int
    estado: str = "disponible"
    id_laboratorio: int


class ResourceUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    codigo: Optional[str] = None
    cantidad_total: Optional[int] = None
    cantidad_disponible: Optional[int] = None
    estado: Optional[str] = None
    id_laboratorio: Optional[int] = None


class ResourceResponse(BaseModel):
    id_recurso: int
    nombre: str
    categoria: Optional[str] = None
    codigo: Optional[str] = None
    cantidad_total: Optional[int] = None
    cantidad_disponible: Optional[int] = None
    estado: Optional[str] = None
    id_laboratorio: Optional[int] = None

    model_config = {"from_attributes": True}
