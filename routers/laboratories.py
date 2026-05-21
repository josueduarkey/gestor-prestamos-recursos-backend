from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/laboratories", tags=["laboratories"])

@router.post("/", response_model=schemas.LaboratoryResponse)
def create_laboratory(laboratory: schemas.LaboratoryCreate, db: Session = Depends(get_db)):
    db_lab = crud.get_laboratory(db, id_laboratorio=laboratory.id_laboratorio)
    if db_lab:
        raise HTTPException(status_code=400, detail="Laboratory already registered")
    return crud.create_laboratory(db=db, laboratory=laboratory)

@router.get("/", response_model=List[schemas.LaboratoryResponse])
def read_laboratories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_laboratories(db, skip=skip, limit=limit)

@router.get("/{id_laboratorio}", response_model=schemas.LaboratoryResponse)
def read_laboratory(id_laboratorio: int, db: Session = Depends(get_db)):
    db_lab = crud.get_laboratory(db, id_laboratorio=id_laboratorio)
    if db_lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return db_lab

@router.put("/{id_laboratorio}", response_model=schemas.LaboratoryResponse)
def update_laboratory(id_laboratorio: int, laboratory: schemas.LaboratoryCreate, db: Session = Depends(get_db)):
    db_lab = crud.update_laboratory(db, id_laboratorio=id_laboratorio, laboratory_update=laboratory)
    if db_lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return db_lab

@router.delete("/{id_laboratorio}", response_model=schemas.LaboratoryResponse)
def delete_laboratory(id_laboratorio: int, db: Session = Depends(get_db)):
    db_lab = crud.delete_laboratory(db, id_laboratorio=id_laboratorio)
    if db_lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return db_lab