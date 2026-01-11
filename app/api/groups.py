from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.group import GroupCreate, GroupOut
from app.models.group import Group
from app.services.group_service import create_group, delete_group

router = APIRouter(prefix="/groups", tags=["Groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GroupOut)
def create(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, group.name)

@router.get("/", response_model=list[GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()

@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(404)
    return group

@router.delete("/{group_id}")
def delete(group_id: int, db: Session = Depends(get_db)):
    if not delete_group(db, group_id):
        raise HTTPException(404)
    return {"status": "deleted"}

@router.get("/{group_id}/students")
def get_students(group_id: int, db: Session = Depends(get_db)):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(404)
    return group.students
