from sqlalchemy import ForeignKey, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

    enrollment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    current_status: Mapped[str] = mapped_column(String(20), default="Active")
    completed_lesson_ids: Mapped[str] = mapped_column(Text, default="[]")  # JSON string list

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
