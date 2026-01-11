from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import students, groups

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students and Groups API")

app.include_router(students.router)
app.include_router(groups.router)
