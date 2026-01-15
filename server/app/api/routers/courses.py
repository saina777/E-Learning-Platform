from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List

from app.db.session import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.enrollment import Enrollment
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/enrolled", response_model=List[CourseResponse])
def get_enrolled_courses(db: Session = Depends(get_db)):
    # For now, use a dummy user_id
    user_id = 1
    
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    course_ids = [e.course_id for e in enrollments]
    
    if not course_ids:
        return []
    
    courses = db.query(Course).filter(Course.id.in_(course_ids)).options(joinedload(Course.instructor)).all()
    
    for course in courses:
        course.lessons_count = db.query(func.count(Lesson.id)).filter(Lesson.course_id == course.id).scalar()
    
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db)
):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in data.dict().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course

@router.patch("/{course_id}", response_model=CourseResponse)
def patch_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db)
):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course

@router.get("/", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).options(joinedload(Course.instructor)).all()
    
    # Add lessons_count to each course
    for course in courses:
        course.lessons_count = db.query(func.count(Lesson.id)).filter(Lesson.course_id == course.id).scalar()
    
    return courses

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()

@router.post("/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_in_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # For now, use a dummy user_id (you'll need to get this from auth token later)
    user_id = 1
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    
    if existing:
        return {"message": "Already enrolled"}
    
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    
    return {"message": "Enrolled successfully"}

@router.delete("/{course_id}/unenroll", status_code=status.HTTP_200_OK)
def unenroll_from_course(course_id: int, db: Session = Depends(get_db)):
    # For now, use a dummy user_id
    user_id = 1
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    db.delete(enrollment)
    db.commit()
    
    return {"message": "Unenrolled successfully"}
