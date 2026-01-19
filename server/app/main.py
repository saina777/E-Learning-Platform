from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_data

from app.api.routers import auth, users, courses, lessons, enrollments, dashboard

app = FastAPI()

from fastapi.responses import Response

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


from app.api.routers import auth
app.include_router(auth.router, prefix="/auth")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_data()


app.include_router(users.router, prefix="/users")
app.include_router(courses.router, prefix="/courses")
app.include_router(lessons.router)
app.include_router(enrollments.router, prefix="/enrollments")
app.include_router(dashboard.router, prefix="/dashboard")


@app.get("/")
def health():
    return {"status": "ok"}
