from fastapi import APIRouter, Depends
from schemas.course import Course
from services import course_service
from fastapi import HTTPException
from core.database import get_db
from supabase import Client

router = APIRouter(tags=["courses"])

@router.get("/", response_model=list[Course])
def get_courses(db : Client = Depends(get_db)):
    return course_service.get_courses(db)

@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int,db : Client = Depends(get_db)):
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=Course)
def create_course( course: Course,db : Client = Depends(get_db)):
    return course_service.create_course(db,course)