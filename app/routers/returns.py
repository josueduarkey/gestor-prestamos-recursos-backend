from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, require_roles
from app.schemas.return_ import ReturnCreate, ReturnResponse
from app.services.return_service import ReturnService

router = APIRouter(prefix="/api/v1/returns", tags=["returns"])


@router.post("/", response_model=ReturnResponse, status_code=201)
def create_return(
    data: ReturnCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return ReturnService(db).create_return(data)


@router.get("/", response_model=List[ReturnResponse])
def list_returns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return ReturnService(db).get_returns(skip=skip, limit=limit)


@router.get("/{id_devolucion}", response_model=ReturnResponse)
def get_return(id_devolucion: int, db: Session = Depends(get_db), _=Depends(require_roles("admin", "gestor"))):
    return ReturnService(db).get_return(id_devolucion)
