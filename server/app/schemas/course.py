from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    price: float
    image_url: Optional[str] = None

class CourseCreateIn(CourseBase):
    pass

class CourseUpdateIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None

class CourseOut(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime
    instructor_name: Optional[str] = None
    lesson_count: Optional[int] = None

    class Config:
        from_attributes = True