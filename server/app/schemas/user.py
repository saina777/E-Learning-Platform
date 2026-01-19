from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr
