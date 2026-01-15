from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app import models  # noqa: F401  (ensures models are imported for table creation)

from app.api.routers import auth  #  import the auth router

app = FastAPI(title="LearnFlow API")
# CORS (must be added before include_router so OPTIONS preflight works)
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

# Create tables (temporary approach; later replace with Alembic migrations)
Base.metadata.create_all(bind=engine)

#  Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "LearnFlow API running"}
