from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.loan import LoanResponse, LoanDetailedResponse, LoanCreate
from app.services.loan_service import LoanService

router = APIRouter(prefix="/api/v1/loans", tags=["loans"])


class LoanCreateRequest(BaseModel):
    id_usuario: int
    responsabilidad: bool
    resource_ids: List[int]


@router.post("/", response_model=LoanResponse, status_code=201)
async def create_loan(
    data: LoanCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    - Admin/Gestor: can create a loan for any user.
    - Estudiante: can only create a loan for themselves (id_usuario is ignored and replaced with their carnet).
    """
    if current_user.role == "estudiante":
        data = LoanCreateRequest(
            id_usuario=current_user.carnet,
            responsabilidad=data.responsabilidad,
            resource_ids=data.resource_ids,
        )
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    loan_data = LoanCreate(id_usuario=data.id_usuario, responsabilidad=data.responsabilidad)
    loan = LoanService(db).create_loan(loan_data, data.resource_ids)

    # Send confirmation email in background
    from app.repositories.user_repository import UserRepository
    from app.repositories.loan_detail_repository import LoanDetailRepository
    from app.services.email_service import send_loan_created_email

    user = UserRepository(db).get_by_carnet(data.id_usuario)
    if user:
        details = LoanDetailRepository(db).get_by_loan(loan.id_loan)
        context = {
            "nombre": user.nombre,
            "carnet": user.carnet,
            "codigo_devolucion": loan.codigo_devolucion,
            "fecha_prestamo": loan.fecha_prestamo.strftime("%d/%m/%Y %H:%M") if loan.fecha_prestamo else "—",
            "fecha_limite": loan.fecha_limite.strftime("%d/%m/%Y %H:%M") if loan.fecha_limite else "—",
            "recursos": [
                {"nombre": d.resource.nombre, "codigo": d.resource.codigo, "cantidad": d.cantidad}
                for d in details if d.resource
            ],
        }
        background_tasks.add_task(send_loan_created_email, user.correo, context)

    return loan


@router.get("/", response_model=List[LoanResponse])
def list_loans(
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    estado: Optional[str] = None,
    overdue_only: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    - Admin/Gestor: can see all loans. Filter by id_usuario, estado, overdue_only.
    - Estudiante: automatically filtered to their own loans.
    """
    if current_user.role == "estudiante":
        id_usuario = current_user.carnet
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    return LoanService(db).get_loans(
        skip=skip, limit=limit, id_usuario=id_usuario, estado=estado, overdue_only=overdue_only
    )


@router.get("/{id_loan}", response_model=LoanDetailedResponse)
def get_loan(id_loan: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Returns loan detail with borrowed resources and return info."""
    loan_detail = LoanService(db).get_loan_with_details(id_loan)
    if current_user.role == "estudiante" and loan_detail["id_usuario"] != current_user.carnet:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot view another user's loan")
    return loan_detail


@router.patch("/{id_loan}/close", response_model=LoanResponse)
def close_loan(
    id_loan: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return LoanService(db).close_loan(id_loan)
