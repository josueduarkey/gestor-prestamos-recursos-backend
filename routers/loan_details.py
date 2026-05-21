from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/loan-details", tags=["loan_details"])

@router.post("/", response_model=schemas.LoanDetailResponse)
def create_loan_detail(loan_detail: schemas.LoanDetailCreate, db: Session = Depends(get_db)):
    db_prestamo = crud.get_prestamo(db, id_prestamo=loan_detail.id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo not found")
    db_resource = crud.get_resource(db, id_recurso=loan_detail.id_recurso)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return crud.create_loan_detail(db=db, loan_detail=loan_detail)

@router.get("/", response_model=List[schemas.LoanDetailResponse])
def read_loan_details(
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_loan_details(db, skip=skip, limit=limit, id_prestamo=id_prestamo)

@router.get("/{id_detalle}", response_model=schemas.LoanDetailResponse)
def read_loan_detail(id_detalle: int, db: Session = Depends(get_db)):
    db_detail = crud.get_loan_detail(db, id_detalle=id_detalle)
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Loan detail not found")
    return db_detail

@router.put("/{id_detalle}", response_model=schemas.LoanDetailResponse)
def update_loan_detail(id_detalle: int, loan_detail: schemas.LoanDetailCreate, db: Session = Depends(get_db)):
    db_detail = crud.update_loan_detail(db, id_detalle=id_detalle, loan_detail_update=loan_detail)
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Loan detail not found")
    return db_detail

@router.delete("/{id_detalle}", response_model=schemas.LoanDetailResponse)
def delete_loan_detail(id_detalle: int, db: Session = Depends(get_db)):
    db_detail = crud.delete_loan_detail(db, id_detalle=id_detalle)
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Loan detail not found")
    return db_detail