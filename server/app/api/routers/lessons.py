from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user, require_instructor
from app.models.lesson import Lesson
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.schemas.lesson import LessonCreateIn as LessonCreate, LessonUpdateIn as LessonUpdate, LessonOut as LessonSchema

router = APIRouter()

@router.get("/courses/{course_id}/lessons", response_model=List[LessonSchema])
def get_course_lessons(
    course_id: int,
    db: Session = Depends(get_db)
):
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    # Return lessons for anyone (public view)
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order_sequence).all()
    return lessons

@router.get("/lessons/{lesson_id}", response_model=LessonSchema)
def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    
    if current_user.role == "instructor" and course.instructor_id == current_user.id:
        pass
    else:
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == lesson.course_id
        ).first()
        if not enrollment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enrolled in this course")
    
    return lesson

@router.post("/courses/{course_id}/lessons", response_model=LessonSchema, status_code=status.HTTP_201_CREATED)
def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id, Course.instructor_id == instructor.id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    lesson = Lesson(
        lesson_title=lesson_data.lesson_title,
        content_body=lesson_data.content_body,
        video_link=lesson_data.video_link,
        order_sequence=lesson_data.order_sequence,
        section_title=lesson_data.section_title,
        course_id=course_id
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

@router.put("/lessons/{lesson_id}", response_model=LessonSchema)
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).join(Course).filter(
        Lesson.id == lesson_id,
        Course.instructor_id == instructor.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    
    for field, value in lesson_data.dict(exclude_unset=True).items():
        setattr(lesson, field, value)
    
    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    instructor: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).join(Course).filter(
        Lesson.id == lesson_id,
        Course.instructor_id == instructor.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}