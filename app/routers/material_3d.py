from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.material_3d import Material3DCreate, Material3DUpdate, Material3DResponse
from app.services.material_3d_service import Material3DService

router = APIRouter(prefix="/api/v1/materials-3d", tags=["materials-3d"])


@router.post("/", response_model=Material3DResponse, status_code=201)
def create_material(data: Material3DCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return Material3DService(db).create_material(data)


@router.get("/", response_model=List[Material3DResponse])
def list_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return Material3DService(db).get_materials(skip=skip, limit=limit)


@router.get("/{id_material}", response_model=Material3DResponse)
def get_material(id_material: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return Material3DService(db).get_material(id_material)


@router.put("/{id_material}", response_model=Material3DResponse)
def update_material(
    id_material: int,
    data: Material3DUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return Material3DService(db).update_material(id_material, data)


@router.delete("/{id_material}", response_model=Material3DResponse)
def delete_material(id_material: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return Material3DService(db).delete_material(id_material)
