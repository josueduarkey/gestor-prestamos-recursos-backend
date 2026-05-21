from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, carnet=user.carnet)
    if db_user:
        raise HTTPException(status_code=400, detail="Carnet already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{carnet}", response_model=schemas.UserResponse)
def read_user(carnet: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, carnet=carnet)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{carnet}", response_model=schemas.UserResponse)
def update_user(carnet: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, carnet=carnet, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{carnet}", response_model=schemas.UserResponse)
def delete_user(carnet: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, carnet=carnet)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user