from pydantic import BaseModel
from typing import Optional


class Material3DCreate(BaseModel):
    tipo_material: str
    descripcion: Optional[str] = None


class Material3DUpdate(BaseModel):
    tipo_material: Optional[str] = None
    descripcion: Optional[str] = None


class Material3DResponse(BaseModel):
    id_material: int
    tipo_material: str
    descripcion: Optional[str] = None

    model_config = {"from_attributes": True}
