from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.printing_3d import Printing3D


class Printing3DRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_impresion: int) -> Optional[Printing3D]:
        return self.db.query(Printing3D).filter(Printing3D.id_impresion == id_impresion).first()

    def get_by_loan(self, id_loan: int) -> Optional[Printing3D]:
        return self.db.query(Printing3D).filter(Printing3D.id_loan == id_loan).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        id_material: Optional[int] = None,
        codigo_impresora: Optional[str] = None,
    ) -> List[Printing3D]:
        query = self.db.query(Printing3D)
        if id_material is not None:
            query = query.filter(Printing3D.id_material == id_material)
        if codigo_impresora:
            query = query.filter(Printing3D.codigo_impresora == codigo_impresora)
        return query.offset(skip).limit(limit).all()

    def create(self, printing: Printing3D) -> Printing3D:
        self.db.add(printing)
        self.db.commit()
        self.db.refresh(printing)
        return printing

    def save(self, printing: Printing3D) -> Printing3D:
        self.db.commit()
        self.db.refresh(printing)
        return printing
