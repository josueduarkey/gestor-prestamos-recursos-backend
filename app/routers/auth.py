from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_email(data.correo)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token({"sub": str(user.carnet), "role": user.role})
    return TokenResponse(access_token=token)


@router.post("/logout")
def logout(_=Depends(get_current_user)):
    """JWT is stateless — the client must delete the token on their side."""
    return {"message": "Logged out successfully. Please clear your token."}
