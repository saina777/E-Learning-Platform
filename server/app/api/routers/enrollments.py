from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.enrollment import Enrollment
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def enroll_course(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    new_enrollment = Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


@router.get("/", response_model=List[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()

@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    enrollment = db.query(Enrollment).get(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(enrollment, key, value)

    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).get(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()
