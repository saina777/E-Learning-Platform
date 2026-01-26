from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EnrollmentCreateIn(BaseModel):
    course_id: int

class EnrollmentUpdateIn(BaseModel):
    current_status: Optional[str] = None

class EnrollmentProgressIn(BaseModel):
    lesson_id: int
    completed: bool

class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrollment_date: datetime
    current_status: str
    completed_lesson_ids_json: str
    last_lesson_id: Optional[int] = None
    course_title: Optional[str] = None
    progress_percent: Optional[float] = None

    class Config:
        from_attributes = True