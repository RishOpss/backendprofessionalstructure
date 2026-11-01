from repository import courses_repository
from schemas.course import Course
from postgrest.exceptions import APIError
from fastapi import HTTPException ,status

async def get_courses(db):
    return await courses_repository.get_all(db)

async def get_course_by_id(db, course_id: int):
    try:
        course = await courses_repository.get_by_id(course_id, db)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course not found"
            )

        return course
    except HTTPException:
        raise

async def create_course(db, course: Course):
    return await courses_repository.create(db,course)

async def delete_course(db, course_id: int):
    course = await courses_repository.get_by_id(course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course not found"
        )
    try:
        response = db.table("courses").delete().eq("course_id", course_id).execute()
        return response.data[0] if response.data else None
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete course: {e}"
        )