from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.session import SessionLocal
from app.core.security import decode_token
from app.models.user import User
from app.models.enrollment import Enrollment
from app.models.course import Course

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_instructor(user: User = Depends(get_current_user)):
    if user.role != "instructor":
        raise HTTPException(status_code=403, detail="Instructor access required")
    return user

def ensure_enrolled_or_instructor(user: User, course: Course, db: Session):
    if user.role == "instructor" and course.instructor_id == user.id:
        return
    enrollment = (
        db.query(Enrollment)
        .filter_by(user_id=user.id, course_id=course.id)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=403, detail="Not Enrolled")
