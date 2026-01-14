from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonResponse
from typing import List

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@router.get("/", response_model=List[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()
