from repository import courses_repository
from schemas.course import Course
from postgrest.exceptions import APIError
from fastapi import HTTPException ,status

async def get_courses(db):
    return await courses_repository.get_all(db)

async def get_course_by_id(course_id: int,db):
    try:
        course = courses_repository.get_by_id(db,course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course not found"
            )

        return await course
    except HTTPException:
        raise

       

async def create_course(course: Course,db):
    return await courses_repository.create(db,course)
