from fastapi import APIRouter , Depends ,BackgroundTasks
from schemas.course import Course
from services import course_service
from dependencies.db import get_db
from background_task.course_task import send_course_creation_email
router = APIRouter(tags=["courses"])

@router.get("/", response_model=list[Course])
async def get_courses(db= Depends(get_db)):
    return await course_service.get_courses(db)

@router.get("/{course_id}", response_model=Course)
async def get_course_by_id(course_id: int,db= Depends(get_db)):
    course = await course_service.get_course_by_id(db,course_id)
    return course

@router.post("/", response_model=Course)
async def create_course(course: Course,background_task:BackgroundTasks, db= Depends(get_db)):
    
    create_course = await course_service.create_course(db, course)
    admin_email ="rishabh@gmail.com"
    background_task.add_task(
        send_course_creation_email,
        create_course["name"],
        admin_email
    )
    return create_course
@router.delete("/{course_id}")
async def delete_course(course_id: int, db= Depends(get_db)):
    deleted_course = await course_service.delete_course(db, course_id)
    return deleted_course