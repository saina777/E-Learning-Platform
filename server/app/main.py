from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_data

from app.api.routers import auth, users, courses, lessons, enrollments, dashboard

app = FastAPI()

from fastapi.responses import Response

from app.api.routers import auth  #  import the auth router

app = FastAPI(title="LearnFlow API")
# CORS (must be added before include_router so OPTIONS preflight works)
from app.api.routers import auth  # ✅ import the auth router
from app.api.routers import courses, lessons, enrollments, dashboard



app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(enrollments.router)
app.include_router(dashboard.router)

# ✅ CORS (must be added before include_router so OPTIONS preflight works)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (temporary approach; later replace with Alembic migrations)
Base.metadata.create_all(bind=engine)
seed_data()


app.include_router(users.router, prefix="/users")
app.include_router(courses.router, prefix="/courses")
app.include_router(lessons.router)
app.include_router(enrollments.router, prefix="/enrollments")
app.include_router(dashboard.router, prefix="/dashboard")

#  Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def health():
    return {"status": "ok"}
