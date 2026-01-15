from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/progress", tags=["Progress"])

# Fake in-memory storage (replace with DB later)
ENROLLMENTS = {
    # course_id: { user_id: [lesson_ids] }
}

LESSONS = {
    1: [
        {"id": 1, "title": "Intro"},
        {"id": 2, "title": "Basics"},
        {"id": 3, "title": "Advanced"}
    ]
}


class ProgressUpdate(BaseModel):
    user_id: int
    lesson_id: int


@router.get("/{course_id}")
def get_progress(course_id: int, user_id: int):
    completed = ENROLLMENTS.get(course_id, {}).get(user_id, [])
    return {
        "lessons": LESSONS.get(course_id, []),
        "completed_lessons": completed
    }


@router.patch("/{course_id}")
def mark_complete(course_id: int, data: ProgressUpdate):
    course = ENROLLMENTS.setdefault(course_id, {})
    lessons = course.setdefault(data.user_id, [])

    if data.lesson_id not in lessons:
        lessons.append(data.lesson_id)

    return {"status": "updated"}


@router.get("/summary")
def progress_summary(user_id: int):
    summary = []

    for course_id, users in ENROLLMENTS.items():
        completed = len(users.get(user_id, []))
        total = len(LESSONS.get(course_id, []))
        summary.append({
            "course_id": course_id,
            "completed": completed,
            "total": total
        })

    return summary
