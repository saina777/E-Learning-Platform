from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.api.deps import get_db, get_current_user
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
import json

router = APIRouter()

@router.get("/")
def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()
    
    dashboard_data = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        lesson_count = db.query(Lesson).filter(Lesson.course_id == course.id).count()
        completed_ids = json.loads(enrollment.completed_lesson_ids_json or "[]")
        progress_percent = (len(completed_ids) / lesson_count * 100) if lesson_count > 0 else 0
        
        dashboard_data.append({
            "enrollment_id": enrollment.id,
            "course_id": course.id,
            "course_title": course.title,
            "course_category": course.category,
            "current_status": enrollment.current_status,
            "progress_percent": progress_percent,
            "total_lessons": lesson_count,
            "last_lesson_id": enrollment.last_lesson_id,
            "lesson_count": lesson_count
        })
    
    return {"enrollments": dashboard_data}