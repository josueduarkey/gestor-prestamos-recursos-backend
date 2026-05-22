from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.return_ import Return
from app.models.loan import Loan


class ReturnRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_devolucion: int) -> Optional[Return]:
        return self.db.query(Return).filter(Return.id_devolucion == id_devolucion).first()

    def get_by_loan(self, id_loan: int) -> Optional[Return]:
        return self.db.query(Return).filter(Return.id_loan == id_loan).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Return]:
        return self.db.query(Return).offset(skip).limit(limit).all()

    def get_by_usuario(self, id_usuario: int, skip: int = 0, limit: int = 100) -> List[Return]:
        return (
            self.db.query(Return)
            .join(Loan, Return.id_loan == Loan.id_loan)
            .filter(Loan.id_usuario == id_usuario)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, return_: Return) -> Return:
        self.db.add(return_)
        self.db.commit()
        self.db.refresh(return_)
        return return_

    def save(self, return_: Return) -> Return:
        self.db.commit()
        self.db.refresh(return_)
        return return_
