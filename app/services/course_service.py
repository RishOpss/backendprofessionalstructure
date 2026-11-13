from repository import courses_repository
from schemas.course import Course
from postgrest.exceptions import APIError
from fastapi import HTTPException ,status
import logging

logger = logging.getLogger("fastapi_application")

async def get_courses(db):
    logger.info("Fetching all courses")
    return await courses_repository.get_all(db)

async def get_course_by_id(db,course_id: int):
    logger.info(f"Fetching course with ID: {course_id}")
    try:
        course = await courses_repository.get_by_id(db, course_id)
        if not course:
            logger.info(f"Course not found of id {course_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course not found"
            )

        return course
    except HTTPException:
        raise

async def create_course(db,course: Course):
    logger.info("Creating new course")
    return await courses_repository.create(db, course)

async def delete_course(db, course_id: int):
    logger.info(f"Deleting course with ID: {course_id}")
    deleted = await courses_repository.delete(db, course_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return deleted
