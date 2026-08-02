from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_students():
    return {"message": "Student Router Working"}


@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student created successfully",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "age": new_student.age
        }
    }