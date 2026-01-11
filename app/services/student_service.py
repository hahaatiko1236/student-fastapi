from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.group import Group

def create_student(db: Session, name: str):
    student = Student(name=name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.get(Student, student_id)
    if student:
        db.delete(student)
        db.commit()
    return student

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.get(Student, student_id)
    group = db.get(Group, group_id)
    student.group = group
    db.commit()
    return student

def remove_student_from_group(db: Session, student_id: int):
    student = db.get(Student, student_id)
    student.group = None
    db.commit()
    return student

def transfer_student(db: Session, student_id: int, new_group_id: int):
    return add_student_to_group(db, student_id, new_group_id)
