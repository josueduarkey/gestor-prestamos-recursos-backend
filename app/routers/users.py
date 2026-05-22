from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.user import UserCreate, UserUpdate, UserResponse, ApplyPenaltyRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Public self-registration. Always creates an 'estudiante' account."""
    return UserService(db).register_student(data)


@router.post("/staff", response_model=UserResponse, status_code=201)
def create_staff_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    """Admin-only. Creates gestor or admin accounts."""
    return UserService(db).create_staff_user(data)


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    has_penalties: bool = False,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    """List users. Filter by role or has_penalties=true."""
    return UserService(db).get_users(skip=skip, limit=limit, role=role, has_penalties=has_penalties)


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{carnet}", response_model=UserResponse)
def get_user(carnet: int, db: Session = Depends(get_db), _=Depends(require_roles("admin", "gestor"))):
    return UserService(db).get_user(carnet)


@router.put("/{carnet}", response_model=UserResponse)
def update_user(
    carnet: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return UserService(db).update_user(carnet, data)


@router.post("/{carnet}/penalties", response_model=UserResponse)
def apply_penalty(
    carnet: int,
    data: ApplyPenaltyRequest,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    """Admin manually applies penalties to a user."""
    return UserService(db).apply_penalty(carnet, data.cantidad)


@router.post("/{carnet}/reset-penalties", response_model=UserResponse)
def reset_penalties(
    carnet: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    """Admin resets a user's penalty count to zero."""
    return UserService(db).reset_penalties(carnet)


@router.delete("/{carnet}", response_model=UserResponse)
def delete_user(carnet: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return UserService(db).delete_user(carnet)
