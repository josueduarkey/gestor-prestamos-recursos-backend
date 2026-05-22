from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, require_roles
from app.schemas.printing_3d import Printing3DCreate, Printing3DUpdate, Printing3DResponse
from app.services.printing_3d_service import Printing3DService

router = APIRouter(prefix="/api/v1/printings-3d", tags=["printings-3d"])


@router.post("/", response_model=Printing3DResponse, status_code=201)
def create_printing(
    data: Printing3DCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).create_printing(data)


@router.get("/", response_model=List[Printing3DResponse])
def list_printings(
    skip: int = 0,
    limit: int = 100,
    id_material: Optional[int] = None,
    codigo_impresora: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).get_printings(
        skip=skip, limit=limit, id_material=id_material, codigo_impresora=codigo_impresora
    )


@router.get("/{id_impresion}", response_model=Printing3DResponse)
def get_printing(
    id_impresion: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).get_printing(id_impresion)


@router.put("/{id_impresion}", response_model=Printing3DResponse)
def update_printing(
    id_impresion: int,
    data: Printing3DUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).update_printing(id_impresion, data)
