import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.loan_repository import LoanRepository
from app.repositories.loan_detail_repository import LoanDetailRepository
from app.repositories.resource_repository import ResourceRepository
from app.repositories.user_repository import UserRepository
from app.models.loan import Loan
from app.models.loan_detail import LoanDetail
from app.schemas.loan import LoanCreate
from typing import Optional, List

MAX_PENALTIES = 3


def _as_utc(dt: datetime) -> datetime:
    """Ensure a datetime is timezone-aware (UTC)."""
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = LoanRepository(db)
        self.detail_repo = LoanDetailRepository(db)
        self.resource_repo = ResourceRepository(db)
        self.user_repo = UserRepository(db)

    def create_loan(self, data: LoanCreate, resource_ids: List[int]) -> Loan:
        if not resource_ids:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "At least one resource is required")

        user = self.user_repo.get_by_carnet(data.id_usuario)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        # Block if user exceeded penalty limit
        if (user.penalizaciones or 0) >= MAX_PENALTIES:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"User has {user.penalizaciones} penalties and cannot borrow. Limit is {MAX_PENALTIES}.",
            )

        # Block if user has an overdue active loan
        now = datetime.now(timezone.utc)
        active_loans = self.repo.get_all(id_usuario=data.id_usuario, estado="activo")
        for existing in active_loans:
            if existing.fecha_limite and _as_utc(existing.fecha_limite) < now:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    "User has an overdue loan. Return it before borrowing again.",
                )

        # Validate all resources have stock
        resources = []
        for rid in resource_ids:
            resource = self.resource_repo.get_by_id(rid)
            if not resource:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"Resource {rid} not found")
            if (resource.cantidad_disponible or 0) < 1:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Resource '{resource.nombre}' has no available stock",
                )
            resources.append(resource)

        # Create loan
        loan = Loan(
            id_usuario=data.id_usuario,
            codigo_devolucion=str(uuid.uuid4())[:8].upper(),
            responsabilidad=data.responsabilidad,
            fecha_prestamo=now,
            fecha_limite=now + timedelta(days=1),
        )
        loan = self.repo.create(loan)

        # Create loan detail per resource and decrement stock
        for resource in resources:
            self.detail_repo.create(
                LoanDetail(id_loan=loan.id_loan, id_recurso=resource.id_recurso, cantidad=1)
            )
            resource.cantidad_disponible -= 1
            if resource.cantidad_disponible == 0:
                resource.estado = "prestado"
            self.resource_repo.save(resource)

        return loan

    def get_loan(self, id_loan: int) -> Loan:
        loan = self.repo.get_by_id(id_loan)
        if not loan:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
        return loan

    def get_loans(
        self,
        skip: int = 0,
        limit: int = 100,
        id_usuario: Optional[int] = None,
        estado: Optional[str] = None,
        overdue_only: bool = False,
    ):
        loans = self.repo.get_all(skip=skip, limit=limit, id_usuario=id_usuario, estado=estado)
        if overdue_only:
            now = datetime.now(timezone.utc)
            loans = [
                l for l in loans
                if l.estado == "activo" and l.fecha_limite and _as_utc(l.fecha_limite) < now
            ]
        return loans

    def close_loan(self, id_loan: int) -> Loan:
        loan = self.get_loan(id_loan)
        if loan.estado != "activo":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Loan is not active")
        loan.estado = "finalizado"
        return self.repo.save(loan)
