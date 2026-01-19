from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    lesson_title: str
    content_body: str
    video_link: str
    order_sequence: int
    section_title: Optional[str] = None

class LessonCreateIn(LessonBase):
    pass

class LessonUpdateIn(BaseModel):
    lesson_title: Optional[str] = None
    content_body: Optional[str] = None
    video_link: Optional[str] = None
    order_sequence: Optional[int] = None
    section_title: Optional[str] = None

class LessonOut(LessonBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True