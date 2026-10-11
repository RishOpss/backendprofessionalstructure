from fastapi import APIRouter
from repository import courses_repository
from services import course_service

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
def get_courses():
    # Logic to retrieve courses from the database
    return course_service.get_courses()

