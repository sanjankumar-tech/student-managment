from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    age: int

class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True