from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.laboratory_repository import LaboratoryRepository
from app.models.laboratory import Laboratory
from app.schemas.laboratory import LaboratoryCreate, LaboratoryUpdate


class LaboratoryService:
    def __init__(self, db: Session):
        self.repo = LaboratoryRepository(db)

    def create_laboratory(self, data: LaboratoryCreate) -> Laboratory:
        if self.repo.get_by_name(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Laboratory already exists")
        lab = Laboratory(nombre=data.nombre)
        return self.repo.create(lab)

    def get_laboratory(self, id_laboratorio: int) -> Laboratory:
        lab = self.repo.get_by_id(id_laboratorio)
        if not lab:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laboratory not found")
        return lab

    def get_laboratories(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)

    def update_laboratory(self, id_laboratorio: int, data: LaboratoryUpdate) -> Laboratory:
        lab = self.get_laboratory(id_laboratorio)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(lab, field, value)
        return self.repo.save(lab)

    def delete_laboratory(self, id_laboratorio: int) -> Laboratory:
        lab = self.get_laboratory(id_laboratorio)
        return self.repo.delete(lab)
