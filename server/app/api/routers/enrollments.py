from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.user import User
from app.schemas import EnrollmentCreate as EnrollmentCreateIn, EnrollmentUpdate as EnrollmentUpdateIn, ProgressUpdate as EnrollmentProgressIn, Enrollment as EnrollmentSchema
import json

router = APIRouter()

@router.post("/", response_model=EnrollmentSchema, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    enrollment_data: EnrollmentCreateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can enroll")
    
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == enrollment_data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already enrolled")
    
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id,
        current_status="Active"
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.get("/me", response_model=List[EnrollmentSchema])
def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()
    return enrollments

@router.delete("/{enrollment_id}")
def unenroll_from_course(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Unenrolled successfully"}

@router.patch("/{enrollment_id}", response_model=EnrollmentSchema)
def update_enrollment_status(
    enrollment_id: int,
    enrollment_data: EnrollmentUpdateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    
    if enrollment_data.current_status:
        enrollment.current_status = enrollment_data.current_status
    
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.patch("/{enrollment_id}/progress", response_model=EnrollmentSchema)
def update_progress(
    enrollment_id: int,
    progress_data: EnrollmentProgressIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    
    completed_ids = json.loads(enrollment.completed_lesson_ids_json or "[]")
    if progress_data.completed:
        if progress_data.lesson_id not in completed_ids:
            completed_ids.append(progress_data.lesson_id)
    else:
        if progress_data.lesson_id in completed_ids:
            completed_ids.remove(progress_data.lesson_id)
    
    enrollment.completed_lesson_ids_json = json.dumps(completed_ids)
    enrollment.last_lesson_id = progress_data.lesson_id
    
    db.commit()
    db.refresh(enrollment)
    return enrollment