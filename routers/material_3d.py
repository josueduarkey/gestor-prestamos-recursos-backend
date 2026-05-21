from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/material-3d", tags=["material_3D"])

@router.post("/", response_model=schemas.Material3DResponse)
def create_material(material: schemas.Material3DCreate, db: Session = Depends(get_db)):
    db_material = crud.get_material_3d(db, id_material=material.id_material)
    if db_material:
        raise HTTPException(status_code=400, detail="Material already registered")
    return crud.create_material_3d(db=db, material=material)

@router.get("/", response_model=List[schemas.Material3DResponse])
def read_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_materials_3d(db, skip=skip, limit=limit)

@router.get("/{id_material}", response_model=schemas.Material3DResponse)
def read_material(id_material: int, db: Session = Depends(get_db)):
    db_material = crud.get_material_3d(db, id_material=id_material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

@router.put("/{id_material}", response_model=schemas.Material3DResponse)
def update_material(id_material: int, material: schemas.Material3DCreate, db: Session = Depends(get_db)):
    db_material = crud.update_material_3d(db, id_material=id_material, material_update=material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

@router.delete("/{id_material}", response_model=schemas.Material3DResponse)
def delete_material(id_material: int, db: Session = Depends(get_db)):
    db_material = crud.delete_material_3d(db, id_material=id_material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material