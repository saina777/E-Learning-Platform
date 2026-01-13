from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lesson_title: Mapped[str] = mapped_column(String(150))
    content_body: Mapped[str] = mapped_column(Text)
    video_link: Mapped[str] = mapped_column(String(255))
    order_sequence: Mapped[int] = mapped_column(Integer)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course = relationship("Course", back_populates="lessons")
