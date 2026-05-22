from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.material_3d_repository import Material3DRepository
from app.models.material_3d import Material3D
from app.schemas.material_3d import Material3DCreate, Material3DUpdate

VALID_MATERIALS = {"PLA", "TPU", "ASA"}


class Material3DService:
    def __init__(self, db: Session):
        self.repo = Material3DRepository(db)

    def create_material(self, data: Material3DCreate) -> Material3D:
        if data.tipo_material not in VALID_MATERIALS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid material. Valid: {VALID_MATERIALS}",
            )
        material = Material3D(**data.model_dump())
        return self.repo.create(material)

    def get_material(self, id_material: int) -> Material3D:
        material = self.repo.get_by_id(id_material)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return material

    def get_materials(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)

    def update_material(self, id_material: int, data: Material3DUpdate) -> Material3D:
        material = self.get_material(id_material)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(material, field, value)
        return self.repo.save(material)

    def delete_material(self, id_material: int) -> Material3D:
        material = self.get_material(id_material)
        return self.repo.delete(material)
