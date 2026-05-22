from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.utils.validators import is_institutional_email
from typing import Optional

VALID_ROLES = {"admin", "gestor", "estudiante"}
MAX_PENALTIES = 3


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def _validate_email(self, correo: str) -> None:
        if not is_institutional_email(correo):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Only @keytest.edu.sv emails are allowed",
            )

    def _check_duplicates(self, carnet: int, correo: str) -> None:
        if self.repo.get_by_carnet(carnet):
            raise HTTPException(status.HTTP_409_CONFLICT, "Carnet already registered")
        if self.repo.get_by_email(correo):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    def _build_user(self, data: UserCreate, role: str) -> User:
        return User(
            carnet=data.carnet,
            nombre=data.nombre,
            correo=data.correo,
            password=hash_password(data.password),
            generacion=data.generacion,
            role=role,
        )

    def register_student(self, data: UserCreate) -> User:
        """Public self-registration — always creates estudiante."""
        self._validate_email(data.correo)
        self._check_duplicates(data.carnet, data.correo)
        return self.repo.create(self._build_user(data, role="estudiante"))

    def create_staff_user(self, data: UserCreate) -> User:
        """Admin-only — creates gestor or admin accounts."""
        self._validate_email(data.correo)
        if data.role not in VALID_ROLES:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid role. Valid: {VALID_ROLES}")
        self._check_duplicates(data.carnet, data.correo)
        return self.repo.create(self._build_user(data, role=data.role))

    def get_user(self, carnet: int) -> User:
        user = self.repo.get_by_carnet(carnet)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        has_penalties: bool = False,
    ):
        return self.repo.get_all(skip=skip, limit=limit, role=role, has_penalties=has_penalties)

    def update_user(self, carnet: int, data: UserUpdate) -> User:
        user = self.get_user(carnet)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return self.repo.save(user)

    def apply_penalty(self, carnet: int, cantidad: int = 1) -> User:
        """Admin manually applies penalties to a user."""
        if cantidad < 1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "cantidad must be at least 1")
        user = self.get_user(carnet)
        user.penalizaciones = (user.penalizaciones or 0) + cantidad
        return self.repo.save(user)

    def reset_penalties(self, carnet: int) -> User:
        user = self.get_user(carnet)
        user.penalizaciones = 0
        return self.repo.save(user)

    def delete_user(self, carnet: int) -> User:
        user = self.get_user(carnet)
        return self.repo.delete(user)
