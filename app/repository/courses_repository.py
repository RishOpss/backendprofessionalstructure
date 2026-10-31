from dependencies.db import get_db
from schemas.course import Course

def get_all(db):
    response = db.table("courses").select("*").execute()
    return response.data

def get_by_id(course_id: int,db):
    response = db.table("courses").select("*").eq("course_id", course_id).execute()
    return response.data[0] if response.data else None

def create(db,course: Course):
    response = db.table("courses").insert(course.dict()).execute()
    return response.data[0]
