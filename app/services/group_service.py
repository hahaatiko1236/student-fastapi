from sqlalchemy.orm import Session
from app.models.group import Group

def create_group(db: Session, name: str):
    group = Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def delete_group(db: Session, group_id: int):
    group = db.get(Group, group_id)
    if group:
        db.delete(group)
        db.commit()
    return group
