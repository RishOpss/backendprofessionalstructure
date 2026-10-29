from repository import courses_repository
from schemas.course import Course
from fastapi import HTTPException
from postgrest.exceptions import APIError
from supabase import Client

def get_courses(db : Client):
    return courses_repository.get_all(db)

def get_course_by_id(db : Client,course_id: int):
    try:
        return courses_repository.get_by_id(db , course_id)
    except APIError as e:
        if e.code == "PGRST116":
            raise HTTPException(status_code=404, detail="Course not found")
        raise HTTPException(status_code=500, detail="Failed to retrieve course")        

def create_course(db : Client,course: Course):
    try:
        return courses_repository.create(db, course)
    except APIError as e:
        if e.code == "23505":
            raise HTTPException(
                status_code=409,
                detail=f"Course with id {course.course_id} already exists",
            )
        raise HTTPException(status_code=500, detail="Failed to create course")