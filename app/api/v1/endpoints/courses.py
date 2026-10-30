from fastapi import APIRouter
from schemas.course import Course
from services import course_service
router = APIRouter(tags=["courses"])

@router.get("/", response_model=list[Course])
def get_courses():
    return course_service.get_courses()

@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int):
    course = course_service.get_course_by_id(course_id)
    return course

@router.post("/", response_model=Course)
def create_course(course: Course):
    return course_service.create_course(course)