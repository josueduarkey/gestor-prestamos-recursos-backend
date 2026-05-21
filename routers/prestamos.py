from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.post("/", response_model=schemas.PrestamoResponse)
def create_prestamo(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, carnet=prestamo.id_usuario)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_prestamo(db=db, prestamo=prestamo)

@router.get("/", response_model=List[schemas.PrestamoResponse])
def read_prestamos(
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    estado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return crud.get_prestamos(db, skip=skip, limit=limit, id_usuario=id_usuario, estado=estado)

@router.get("/{id_prestamo}", response_model=schemas.PrestamoResponse)
def read_prestamo(id_prestamo: int, db: Session = Depends(get_db)):
    db_prestamo = crud.get_prestamo(db, id_prestamo=id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    return db_prestamo

@router.put("/{id_prestamo}", response_model=schemas.PrestamoResponse)
def update_prestamo(id_prestamo: int, prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    db_prestamo = crud.update_prestamo(db, id_prestamo=id_prestamo, prestamo_update=prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    return db_prestamo

@router.delete("/{id_prestamo}", response_model=schemas.PrestamoResponse)
def delete_prestamo(id_prestamo: int, db: Session = Depends(get_db)):
    db_prestamo = crud.delete_prestamo(db, id_prestamo=id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    return db_prestamo