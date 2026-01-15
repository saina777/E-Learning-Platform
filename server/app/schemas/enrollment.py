from pydantic import BaseModel
from typing import Optional

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    user_id: Optional[int] = None
    course_id: Optional[int] = None

class EnrollmentResponse(EnrollmentBase):
    id: int
    
    class Config:
        from_attributes = True