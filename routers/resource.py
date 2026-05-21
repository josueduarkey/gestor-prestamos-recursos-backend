from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=schemas.ResourceResponse)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = crud.get_resource_by_codigo(db, codigo=resource.codigo)
    if db_resource:
        raise HTTPException(status_code=400, detail="Resource code already registered")
    return crud.create_resource(db=db, resource=resource)

@router.get("/", response_model=List[schemas.ResourceResponse])
def read_resources(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    id_laboratorio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_resources(db, skip=skip, limit=limit, categoria=categoria, id_laboratorio=id_laboratorio)

@router.get("/{id_recurso}", response_model=schemas.ResourceResponse)
def read_resource(id_recurso: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, id_recurso=id_recurso)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.put("/{id_recurso}", response_model=schemas.ResourceResponse)
def update_resource(id_recurso: int, resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = crud.update_resource(db, id_recurso=id_recurso, resource_update=resource)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.delete("/{id_recurso}", response_model=schemas.ResourceResponse)
def delete_resource(id_recurso: int, db: Session = Depends(get_db)):
    db_resource = crud.delete_resource(db, id_recurso=id_recurso)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource