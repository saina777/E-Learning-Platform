from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))  # Student / Instructor
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reset_token_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    courses = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="user")
