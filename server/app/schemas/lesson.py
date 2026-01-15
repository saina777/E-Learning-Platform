from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    lesson_title: str
    content_body: str
    video_link: str
    order_sequence: int
    course_id: int

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    lesson_title: Optional[str] = None
    content_body: Optional[str] = None
    video_link: Optional[str] = None
    order_sequence: Optional[int] = None

class LessonResponse(LessonBase):
    id: int
    
    class Config:
        from_attributes = True