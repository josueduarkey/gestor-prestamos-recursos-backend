from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.loan_detail import LoanDetail


class LoanDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_detalle: int) -> Optional[LoanDetail]:
        return self.db.query(LoanDetail).filter(LoanDetail.id_detalle == id_detalle).first()

    def get_by_loan(self, id_loan: int) -> List[LoanDetail]:
        return self.db.query(LoanDetail).filter(LoanDetail.id_loan == id_loan).all()

    def create(self, detail: LoanDetail) -> LoanDetail:
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(detail)
        return detail

    def delete(self, detail: LoanDetail) -> LoanDetail:
        self.db.delete(detail)
        self.db.commit()
        return detail
