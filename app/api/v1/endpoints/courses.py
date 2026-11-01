from fastapi import APIRouter , Depends
from schemas.course import Course
from services import course_service
from dependencies.db import get_db

router = APIRouter(tags=["courses"])

@router.get("/", response_model=list[Course])
async def get_courses(db= Depends(get_db)):
    return await course_service.get_courses(db)

@router.get("/{course_id}", response_model=Course)
async def get_course_by_id(course_id: int,db= Depends(get_db)):
    course = await course_service.get_course_by_id(db,course_id)
    return course

@router.post("/", response_model=Course)
def create_course(course: Course, background_tasks: BackgroundTasks, db= Depends(get_db)):
    created_course = course_service.create_course(db, course)

    # Hardcoded administrator email
    admin_email = "rishabh.raj@example.com"

    # Register background task
    background_tasks.add_task(
        send_course_creation_email,
        created_course["name"],
        admin_email
    )

    return created_course