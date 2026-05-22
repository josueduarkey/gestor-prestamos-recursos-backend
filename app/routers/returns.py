from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.return_ import ReturnCreate, ReturnResponse
from app.services.return_service import ReturnService

router = APIRouter(prefix="/api/v1/returns", tags=["returns"])


@router.post("/", response_model=ReturnResponse, status_code=201)
def create_return(
    data: ReturnCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Process a return with optional evidence photo path (from POST /api/v1/uploads/evidence).
    - Admin/Gestor: can process any return.
    - Estudiante: can only return their own loans.
    """
    if current_user.role == "estudiante":
        from app.repositories.loan_repository import LoanRepository
        loan = LoanRepository(db).get_by_id(data.id_loan)
        if not loan or loan.id_usuario != current_user.carnet:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot process return for another user's loan")
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    return ReturnService(db).create_return(data)


@router.get("/", response_model=List[ReturnResponse])
def list_returns(
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    - Admin/Gestor: see all returns. Filter by id_usuario.
    - Estudiante: see only their own return history.
    """
    if current_user.role == "estudiante":
        id_usuario = current_user.carnet
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    return ReturnService(db).get_returns(skip=skip, limit=limit, id_usuario=id_usuario)


@router.get("/{id_devolucion}", response_model=ReturnResponse)
def get_return(
    id_devolucion: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return ReturnService(db).get_return(id_devolucion)
