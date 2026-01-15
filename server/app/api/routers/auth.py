from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

reset_serializer = URLSafeTimedSerializer(settings.JWT_SECRET)
RESET_TOKEN_MAX_AGE_SECONDS = 30 * 60

class RegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    role: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequestIn(BaseModel):
    email: EmailStr


class PasswordResetIn(BaseModel):
    token: str
    new_password: str = Field(min_length=6, max_length=72)


# --------- Routes ----------
@router.post("/register", status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Return safe user data (no password)
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }


@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.post("/request-password-reset")
def request_password_reset(payload: PasswordResetRequestIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    generic_message = {"message": "If the email exists, a reset token has been generated."}
    
    if not user:
        return generic_message
    
    token = reset_serializer.dumps({"user_id": user.id})
    return {**generic_message, "token": token}


@router.post("/reset-password")
def reset_password(payload: PasswordResetIn, db: Session = Depends(get_db)):
    try:
        data = reset_serializer.loads(payload.token, max_age=RESET_TOKEN_MAX_AGE_SECONDS)
        user_id = data.get("user_id")
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Reset token expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(payload.new_password)
    db.commit()

    return {"message": "Password updated successfully"}
