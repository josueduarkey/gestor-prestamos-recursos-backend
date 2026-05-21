from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/printing-3d", tags=["printing_3d"])

@router.post("/", response_model=schemas.Printing3DResponse)
def create_printing(printing: schemas.Printing3DCreate, db: Session = Depends(get_db)):
    db_prestamo = crud.get_prestamo(db, id_prestamo=printing.id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    db_material = crud.get_material_3d(db, id_material=printing.id_material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return crud.create_printing_3d(db=db, printing=printing)

@router.get("/", response_model=List[schemas.Printing3DResponse])
def read_printings(
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
    id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_printings_3d(db, skip=skip, limit=limit, id_prestamo=id_prestamo, id_material=id_material)

@router.get("/{id_impresion}", response_model=schemas.Printing3DResponse)
def read_printing(id_impresion: int, db: Session = Depends(get_db)):
    db_printing = crud.get_printing_3d(db, id_impresion=id_impresion)
    if db_printing is None:
        raise HTTPException(status_code=404, detail="Printing not found")
    return db_printing

@router.put("/{id_impresion}", response_model=schemas.Printing3DResponse)
def update_printing(id_impresion: int, printing: schemas.Printing3DCreate, db: Session = Depends(get_db)):
    db_printing = crud.update_printing_3d(db, id_impresion=id_impresion, printing_update=printing)
    if db_printing is None:
        raise HTTPException(status_code=404, detail="Printing not found")
    return db_printing

@router.delete("/{id_impresion}", response_model=schemas.Printing3DResponse)
def delete_printing(id_impresion: int, db: Session = Depends(get_db)):
    db_printing = crud.delete_printing_3d(db, id_impresion=id_impresion)
    if db_printing is None:
        raise HTTPException(status_code=404, detail="Printing not found")
    return db_printing