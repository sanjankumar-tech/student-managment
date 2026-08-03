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
    @router.get("/{student_id}")
    def get_student(studnet_id: int, db: Session = Depends(get_db)):
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if student is None:
            return {"message": "Student not found"} 
        return student

@router.put("/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if db_student is None:
        return {"message": "Student not found"}

    db_student.name = student.name
    db_student.email = student.email
    db_student.age = student.age

    db.commit()
    db.refresh(db_student)

    return {
        "message": "Student updated successfully",
        "student": db_student
    }
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        return {"message": "Student not found"}

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }