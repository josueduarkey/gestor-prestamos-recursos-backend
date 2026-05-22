from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.loan import Loan


class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_loan: int) -> Optional[Loan]:
        return self.db.query(Loan).filter(Loan.id_loan == id_loan).first()

    def get_by_codigo_devolucion(self, codigo: str) -> Optional[Loan]:
        return self.db.query(Loan).filter(Loan.codigo_devolucion == codigo).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        id_usuario: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Loan]:
        query = self.db.query(Loan)
        if id_usuario is not None:
            query = query.filter(Loan.id_usuario == id_usuario)
        if estado is not None:
            query = query.filter(Loan.estado == estado)
        return query.offset(skip).limit(limit).all()

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def save(self, loan: Loan) -> Loan:
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def delete(self, loan: Loan) -> Loan:
        self.db.delete(loan)
        self.db.commit()
        return loan
