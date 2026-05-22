from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.services.resource_service import ResourceService

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.post("/", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin", "gestor"))):
    return ResourceService(db).create_resource(data)


@router.get("/", response_model=List[ResourceResponse])
def list_resources(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    id_laboratorio: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return ResourceService(db).get_resources(skip=skip, limit=limit, categoria=categoria, id_laboratorio=id_laboratorio, estado=estado)


@router.get("/{id_recurso}", response_model=ResourceResponse)
def get_resource(id_recurso: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return ResourceService(db).get_resource(id_recurso)


@router.put("/{id_recurso}", response_model=ResourceResponse)
def update_resource(
    id_recurso: int,
    data: ResourceUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return ResourceService(db).update_resource(id_recurso, data)


@router.delete("/{id_recurso}", response_model=ResourceResponse)
def delete_resource(id_recurso: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return ResourceService(db).delete_resource(id_recurso)
