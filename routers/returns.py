from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/returns", tags=["returns"])

@router.post("/", response_model=schemas.ReturnResponse)
def create_return(return_data: schemas.ReturnCreate, db: Session = Depends(get_db)):
    db_prestamo = crud.get_prestamo(db, id_prestamo=return_data.id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    return crud.create_return(db=db, return_data=return_data)

@router.get("/", response_model=List[schemas.ReturnResponse])
def read_returns(
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
    estado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return crud.get_returns(db, skip=skip, limit=limit, id_prestamo=id_prestamo, estado=estado)

@router.get("/{id_devolucion}", response_model=schemas.ReturnResponse)
def read_return(id_devolucion: int, db: Session = Depends(get_db)):
    db_return = crud.get_return(db, id_devolucion=id_devolucion)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Return not found")
    return db_return

@router.put("/{id_devolucion}", response_model=schemas.ReturnResponse)
def update_return(id_devolucion: int, return_data: schemas.ReturnCreate, db: Session = Depends(get_db)):
    db_return = crud.update_return(db, id_devolucion=id_devolucion, return_update=return_data)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Return not found")
    return db_return

@router.delete("/{id_devolucion}", response_model=schemas.ReturnResponse)
def delete_return(id_devolucion: int, db: Session = Depends(get_db)):
    db_return = crud.delete_return(db, id_devolucion=id_devolucion)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Return not found")
    return db_return