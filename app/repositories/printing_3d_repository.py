from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.printing_3d import Printing3D


class Printing3DRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_impresion: int) -> Optional[Printing3D]:
        return self.db.query(Printing3D).filter(Printing3D.id_impresion == id_impresion).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        id_usuario: Optional[int] = None,
        id_material: Optional[int] = None,
        id_printer: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Printing3D]:
        query = self.db.query(Printing3D)
        if id_usuario is not None:
            query = query.filter(Printing3D.id_usuario == id_usuario)
        if id_material is not None:
            query = query.filter(Printing3D.id_material == id_material)
        if id_printer is not None:
            query = query.filter(Printing3D.id_printer == id_printer)
        if estado:
            query = query.filter(Printing3D.estado == estado)
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
