from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=72)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    title: str
    description: str
    price: float
    category: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class Course(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Lesson schemas
class LessonBase(BaseModel):
    title: str
    content: str
    video_url: Optional[str] = None
    order_index: int

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    order_index: Optional[int] = None

class Lesson(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enrollment schemas
class EnrollmentBase(BaseModel):
    current_status: str = "active"

class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentUpdate(BaseModel):
    current_status: Optional[str] = None

class ProgressUpdate(BaseModel):
    completed_lessons: Optional[List[int]] = None
    progress_percentage: Optional[float] = None

class Enrollment(EnrollmentBase):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    completed_lessons: Optional[str] = None
    progress_percentage: float = 0.0
    
    class Config:
        from_attributes = True

# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=6, max_length=72)