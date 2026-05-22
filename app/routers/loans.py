from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.loan import LoanResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/api/v1/loans", tags=["loans"])


class LoanCreateRequest(BaseModel):
    id_usuario: int
    responsabilidad: bool
    resource_ids: List[int]


@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan(
    data: LoanCreateRequest,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    from app.schemas.loan import LoanCreate
    loan_data = LoanCreate(id_usuario=data.id_usuario, responsabilidad=data.responsabilidad)
    return LoanService(db).create_loan(loan_data, data.resource_ids)


@router.get("/", response_model=List[LoanResponse])
def list_loans(
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    estado: Optional[str] = None,
    overdue_only: bool = False,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return LoanService(db).get_loans(
        skip=skip, limit=limit, id_usuario=id_usuario, estado=estado, overdue_only=overdue_only
    )


@router.get("/{id_loan}", response_model=LoanResponse)
def get_loan(id_loan: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return LoanService(db).get_loan(id_loan)


@router.patch("/{id_loan}/close", response_model=LoanResponse)
def close_loan(id_loan: int, db: Session = Depends(get_db), _=Depends(require_roles("admin", "gestor"))):
    return LoanService(db).close_loan(id_loan)
