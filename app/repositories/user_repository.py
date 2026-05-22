from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_carnet(self, carnet: int) -> Optional[User]:
        return self.db.query(User).filter(User.carnet == carnet).first()

    def get_by_email(self, correo: str) -> Optional[User]:
        return self.db.query(User).filter(User.correo == correo).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> User:
        self.db.delete(user)
        self.db.commit()
        return user
