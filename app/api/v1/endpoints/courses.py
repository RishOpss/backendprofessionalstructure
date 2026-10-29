from fastapi import APIRouter
from schemas.course import Course
from services import course_service

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=list[Course])
def get_courses():
    return course_service.get_courses()
