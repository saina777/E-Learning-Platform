from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enrollment import Enrollment

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/student/{user_id}")
def student_dashboard(user_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == user_id
    ).all()

    return {
        "user_id": user_id,
        "enrollments": [
            {
                "course_id": e.course_id,
                "enrollment_id": e.id
            } for e in enrollments
        ]
    }
