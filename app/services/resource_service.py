from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.resource_repository import ResourceRepository
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate
from typing import Optional

VALID_ESTADOS = {"disponible", "prestado", "mantenimiento", "dañado"}


class ResourceService:
    def __init__(self, db: Session):
        self.repo = ResourceRepository(db)

    def create_resource(self, data: ResourceCreate) -> Resource:
        if data.codigo and self.repo.get_by_codigo(data.codigo):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resource code already exists")
        if data.estado not in VALID_ESTADOS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid estado. Valid: {VALID_ESTADOS}")

        resource = Resource(**data.model_dump())
        return self.repo.create(resource)

    def get_resource(self, id_recurso: int) -> Resource:
        resource = self.repo.get_by_id(id_recurso)
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        return resource

    def get_resources(
        self,
        skip: int = 0,
        limit: int = 100,
        categoria: Optional[str] = None,
        id_laboratorio: Optional[int] = None,
        estado: Optional[str] = None,
    ):
        return self.repo.get_all(skip=skip, limit=limit, categoria=categoria, id_laboratorio=id_laboratorio, estado=estado)

    def update_resource(self, id_recurso: int, data: ResourceUpdate) -> Resource:
        resource = self.get_resource(id_recurso)
        if data.estado and data.estado not in VALID_ESTADOS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid estado. Valid: {VALID_ESTADOS}")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(resource, field, value)
        return self.repo.save(resource)

    def delete_resource(self, id_recurso: int) -> Resource:
        resource = self.get_resource(id_recurso)
        return self.repo.delete(resource)
