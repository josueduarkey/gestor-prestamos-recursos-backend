from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.laboratory import Laboratory


class LaboratoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_laboratorio: int) -> Optional[Laboratory]:
        return self.db.query(Laboratory).filter(Laboratory.id_laboratorio == id_laboratorio).first()

    def get_by_name(self, nombre: str) -> Optional[Laboratory]:
        return self.db.query(Laboratory).filter(Laboratory.nombre == nombre).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Laboratory]:
        return self.db.query(Laboratory).offset(skip).limit(limit).all()

    def create(self, lab: Laboratory) -> Laboratory:
        self.db.add(lab)
        self.db.commit()
        self.db.refresh(lab)
        return lab

    def save(self, lab: Laboratory) -> Laboratory:
        self.db.commit()
        self.db.refresh(lab)
        return lab

    def delete(self, lab: Laboratory) -> Laboratory:
        self.db.delete(lab)
        self.db.commit()
        return lab
