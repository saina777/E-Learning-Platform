from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse
)

router = APIRouter(prefix="/lessons", tags=["Lessons"])
@router.post("/", response_model=LessonResponse, status_code=201)
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db)
):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_course_lessons(course_id: int, db: Session = Depends(get_db)):
    return db.query(Lesson).filter(
        Lesson.course_id == course_id
    ).all()

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).get(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    for key, value in data.dict().items():
        setattr(lesson, key, value)

    db.commit()
    db.refresh(lesson)
    return lesson


@router.patch("/{lesson_id}", response_model=LessonResponse)
def patch_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).get(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(lesson, key, value)

    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}", status_code=204)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).get(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()
