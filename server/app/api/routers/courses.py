from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user, require_instructor
from app.models.course import Course
from app.models.user import User
from app.schemas import CourseCreate, CourseUpdate, Course as CourseSchema

router = APIRouter()

@router.get("/", response_model=List[CourseSchema])
def get_courses(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if search:
        query = query.filter(Course.title.contains(search))
    if category:
        query = query.filter(Course.category == category)
    courses = query.all()
    return courses

@router.get("/{course_id}", response_model=CourseSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    course = Course(
        title=course_data.title,
        description=course_data.description,
        price=course_data.price,
        category=course_data.category,
        image_url=course_data.image_url,
        learning_outcomes_json=course_data.learning_outcomes_json,
        instructor_id=instructor.id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id, Course.instructor_id == instructor.id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    for field, value in course_data.dict(exclude_unset=True).items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id, Course.instructor_id == instructor.id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}