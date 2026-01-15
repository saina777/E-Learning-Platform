from pydantic import BaseModel
from typing import Optional, List

class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    price: float = 0.0
    instructor_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class InstructorInfo(BaseModel):
    id: int
    full_name: str
    email: str
    
    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    instructor: Optional[InstructorInfo] = None
    lessons_count: int = 0
    
    class Config:
        from_attributes = True