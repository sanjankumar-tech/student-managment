from fastapi import FastAPI
from app.routers.student import router as student_router

from app.database.connection import engine, Base
from app.models.student import Student
from app.routers.student import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student_router)


@app.get("/")
def home():
    return {
        "message": "Student Management API unning Successfully"
    }