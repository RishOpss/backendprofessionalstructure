from repository import courses_repository
from schemas.course import Course
from postgrest.exceptions import APIError
from fastapi import HTTPException ,status
import logging

logger = logging.getLogger("fastapi_application")

def get_courses(db):
    logger.info("Fetching all courses")
    return courses_repository.get_all(db)

def get_course_by_id(db,course_id: int):
    logger.info(f"Fetching course with ID: {course_id}")
    try:
        course = await courses_repository.get_by_id(course_id, db)
        if not course:
            logger.info(f"Course not found of id {course_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course not found"
            )

        return course
    except HTTPException:
        raise

def create_course(db,course: Course):
    logger.info("Creating new course")
    return courses_repository.create(db,course)
