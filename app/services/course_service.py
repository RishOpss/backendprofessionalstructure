from repository import courses_repository
from schemas.course import Course
from fastapi import HTTPException
from postgrest.exceptions import APIError

def get_courses():
    return courses_repository.get_all()

def get_course_by_id(course_id: int):
    try:
        return courses_repository.get_by_id(course_id)
    except APIError as e:
        if e.code == "PGRST116":
            raise HTTPException(status_code=404, detail="Course not found")
        raise HTTPException(status_code=500, detail="Failed to retrieve course")        

def create_course(course: Course):
    try:
        return courses_repository.create(course)
    except APIError as e:
        if e.code == "23505":
            raise HTTPException(
                status_code=409,
                detail=f"Course with id {course.course_id} already exists",
            )
        raise HTTPException(status_code=500, detail="Failed to create course")