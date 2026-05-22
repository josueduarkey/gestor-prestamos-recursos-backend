from pydantic import BaseModel
from typing import Optional


class LoanDetailCreate(BaseModel):
    id_loan: int
    id_recurso: int
    cantidad: int = 1


class LoanDetailUpdate(BaseModel):
    cantidad: Optional[int] = None


class LoanDetailResponse(BaseModel):
    id_detalle: int
    id_loan: int
    id_recurso: int
    cantidad: int

    model_config = {"from_attributes": True}
