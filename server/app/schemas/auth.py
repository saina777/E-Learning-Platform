from pydantic import BaseModel, EmailStr
from .user import UserOut

class RegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "student"

class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
 

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
