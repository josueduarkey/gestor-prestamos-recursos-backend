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

        if (user.penalizaciones or 0) >= MAX_PENALTIES:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"User has {user.penalizaciones} penalties and cannot borrow. Limit is {MAX_PENALTIES}.",
            )

        now = datetime.now(timezone.utc)
        active_loans = self.repo.get_all(id_usuario=data.id_usuario, estado="activo")
        for existing in active_loans:
            if existing.fecha_limite and _as_utc(existing.fecha_limite) < now:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    "User has an overdue loan. Return it before borrowing again.",
                )

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

        fecha_limite = _as_utc(data.fecha_limite) if data.fecha_limite else now + timedelta(days=1)

        loan = Loan(
            id_usuario=data.id_usuario,
            codigo_devolucion=str(uuid.uuid4())[:8].upper(),
            responsabilidad=data.responsabilidad,
            fecha_prestamo=now,
            fecha_limite=fecha_limite,
        )
        loan = self.repo.create(loan)

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

    def get_loan_with_details(self, id_loan: int) -> dict:
        loan = self.get_loan(id_loan)
        now = datetime.now(timezone.utc)
        is_overdue = (
            loan.estado == "activo"
            and loan.fecha_limite is not None
            and _as_utc(loan.fecha_limite) < now
        )

        resources = []
        for detail in loan.loan_details:
            if detail.resource:
                resources.append({
                    "id_recurso": detail.resource.id_recurso,
                    "nombre": detail.resource.nombre,
                    "codigo": detail.resource.codigo,
                    "cantidad": detail.cantidad,
                })

        return_info = None
        if loan.return_:
            r = loan.return_
            return_info = {
                "id_devolucion": r.id_devolucion,
                "fecha_devolucion": r.fecha_devolucion,
                "hay_danios": r.hay_danios,
                "descripcion": r.descripcion,
            }

        return {
            "id_loan": loan.id_loan,
            "id_usuario": loan.id_usuario,
            "codigo_devolucion": loan.codigo_devolucion,
            "responsabilidad": loan.responsabilidad,
            "estado": loan.estado,
            "fecha_prestamo": loan.fecha_prestamo,
            "fecha_limite": loan.fecha_limite,
            "is_overdue": is_overdue,
            "resources": resources,
            "return_info": return_info,
        }

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
