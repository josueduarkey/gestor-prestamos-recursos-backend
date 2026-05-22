from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, require_roles
from app.schemas.laboratory import LaboratoryCreate, LaboratoryUpdate, LaboratoryResponse
from app.services.laboratory_service import LaboratoryService

router = APIRouter(prefix="/api/v1/laboratories", tags=["laboratories"])


@router.post("/", response_model=LaboratoryResponse, status_code=201)
def create_laboratory(data: LaboratoryCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return LaboratoryService(db).create_laboratory(data)


@router.get("/", response_model=List[LaboratoryResponse])
def list_laboratories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return LaboratoryService(db).get_laboratories(skip=skip, limit=limit)


@router.get("/{id_laboratorio}", response_model=LaboratoryResponse)
def get_laboratory(id_laboratorio: int, db: Session = Depends(get_db)):
    return LaboratoryService(db).get_laboratory(id_laboratorio)


@router.put("/{id_laboratorio}", response_model=LaboratoryResponse)
def update_laboratory(
    id_laboratorio: int,
    data: LaboratoryUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return LaboratoryService(db).update_laboratory(id_laboratorio, data)


@router.delete("/{id_laboratorio}", response_model=LaboratoryResponse)
def delete_laboratory(id_laboratorio: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return LaboratoryService(db).delete_laboratory(id_laboratorio)
