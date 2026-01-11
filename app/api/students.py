from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.student import StudentCreate, StudentOut
from app.models.student import Student
from app.services.student_service import (
    create_student,
    delete_student,
    add_student_to_group,
    remove_student_from_group,
    transfer_student
)

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StudentOut)
def create(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student.name)

@router.get("/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(404)
    return student

@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    if not delete_student(db, student_id):
        raise HTTPException(404)
    return {"status": "deleted"}

@router.post("/{student_id}/add-to-group/{group_id}", response_model=StudentOut)
def add_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    return add_student_to_group(db, student_id, group_id)

@router.post("/{student_id}/remove-from-group", response_model=StudentOut)
def remove_from_group(student_id: int, db: Session = Depends(get_db)):
    return remove_student_from_group(db, student_id)

@router.post("/{student_id}/transfer/{group_id}", response_model=StudentOut)
def transfer(student_id: int, group_id: int, db: Session = Depends(get_db)):
    return transfer_student(db, student_id, group_id)
