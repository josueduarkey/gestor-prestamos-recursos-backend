from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.return_repository import ReturnRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.resource_repository import ResourceRepository
from app.repositories.user_repository import UserRepository
from app.models.return_ import Return
from app.schemas.return_ import ReturnCreate


def _as_utc(dt: datetime) -> datetime:
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


class ReturnService:
    def __init__(self, db: Session):
        self.repo = ReturnRepository(db)
        self.loan_repo = LoanRepository(db)
        self.resource_repo = ResourceRepository(db)
        self.user_repo = UserRepository(db)

    def create_return(self, data: ReturnCreate) -> Return:
        loan = self.loan_repo.get_by_id(data.id_loan)
        if not loan:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
        if loan.estado != "activo":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Loan is already closed")
        if self.repo.get_by_loan(data.id_loan):
            raise HTTPException(status.HTTP_409_CONFLICT, "Return already registered for this loan")

        now = datetime.now(timezone.utc)
        is_late = loan.fecha_limite and _as_utc(loan.fecha_limite) < now

        return_ = Return(
            id_loan=data.id_loan,
            fecha_devolucion=now,
            evidencia=data.evidencia,
            descripcion=data.descripcion,
            hay_danios=data.hay_danios,
        )
        return_ = self.repo.create(return_)

        # Close loan
        loan.estado = "finalizado"
        self.loan_repo.save(loan)

        # Restore stock for every resource in the loan
        for detail in loan.loan_details:
            resource = self.resource_repo.get_by_id(detail.id_recurso)
            if resource:
                resource.cantidad_disponible = (resource.cantidad_disponible or 0) + detail.cantidad
                if resource.cantidad_disponible > 0 and resource.estado == "prestado":
                    resource.estado = "disponible"
                self.resource_repo.save(resource)

        # Apply penalties
        user = self.user_repo.get_by_carnet(loan.id_usuario)
        if user:
            if is_late:
                user.penalizaciones = (user.penalizaciones or 0) + 1
            if data.hay_danios:
                user.penalizaciones = (user.penalizaciones or 0) + 1
            self.user_repo.save(user)

        return return_

    def get_return(self, id_devolucion: int) -> Return:
        return_ = self.repo.get_by_id(id_devolucion)
        if not return_:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Return not found")
        return return_

    def get_returns(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)
