from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.resource import Resource


class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_recurso: int) -> Optional[Resource]:
        return self.db.query(Resource).filter(Resource.id_recurso == id_recurso).first()

    def get_by_codigo(self, codigo: str) -> Optional[Resource]:
        return self.db.query(Resource).filter(Resource.codigo == codigo).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        categoria: Optional[str] = None,
        id_laboratorio: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Resource]:
        query = self.db.query(Resource)
        if categoria:
            query = query.filter(Resource.categoria == categoria)
        if id_laboratorio:
            query = query.filter(Resource.id_laboratorio == id_laboratorio)
        if estado:
            query = query.filter(Resource.estado == estado)
        return query.offset(skip).limit(limit).all()

    def create(self, resource: Resource) -> Resource:
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def save(self, resource: Resource) -> Resource:
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def delete(self, resource: Resource) -> Resource:
        self.db.delete(resource)
        self.db.commit()
        return resource
