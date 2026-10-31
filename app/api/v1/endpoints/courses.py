from fastapi import APIRouter , Depends
from schemas.course import Course
from services import course_service
from dependencies.db import get_db

router = APIRouter(tags=["courses"])

@router.get("/", response_model=list[Course])
def get_courses(db= Depends(get_db)):
    return course_service.get_courses(db)

@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int,db= Depends(get_db)):
    course = course_service.get_course_by_id(db,course_id)
    return course

@router.post("/", response_model=Course)
def create_course(course: Course,db= Depends(get_db)):
    return course_service.create_course(db,course)