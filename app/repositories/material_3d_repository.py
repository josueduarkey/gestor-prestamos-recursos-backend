from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.material_3d import Material3D


class Material3DRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_material: int) -> Optional[Material3D]:
        return self.db.query(Material3D).filter(Material3D.id_material == id_material).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Material3D]:
        return self.db.query(Material3D).offset(skip).limit(limit).all()

    def create(self, material: Material3D) -> Material3D:
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def save(self, material: Material3D) -> Material3D:
        self.db.commit()
        self.db.refresh(material)
        return material

    def delete(self, material: Material3D) -> Material3D:
        self.db.delete(material)
        self.db.commit()
        return material
