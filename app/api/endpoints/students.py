from fastapi import APIRouter
from schemas.students import StudentCreate, StudentUpdate
from services import student_service
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
def get_students():
    # Logic to retrieve students from the database
    return  student_service.get_students()

@router.post("/")
def create_student(student: StudentCreate):
    # Logic to create a new student in the database
    return student_service.create_student(student)