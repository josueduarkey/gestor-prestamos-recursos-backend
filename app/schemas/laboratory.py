from pydantic import BaseModel
from typing import Optional


class LaboratoryCreate(BaseModel):
    nombre: str


class LaboratoryUpdate(BaseModel):
    nombre: Optional[str] = None


class LaboratoryResponse(BaseModel):
    id_laboratorio: int
    nombre: str

    model_config = {"from_attributes": True}
