from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app import models

from app.api.routers import auth
from app.api.routers import courses, lessons, enrollments, dashboard

app = FastAPI(title="LearnFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/")
def root():
    return {"message": "LearnFlow API running"}
