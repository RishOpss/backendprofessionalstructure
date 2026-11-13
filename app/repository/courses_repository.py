from dependencies.db import get_db
from schemas.course import Course

async def get_all(db):
    response = db.table("courses").select("*").execute()
    return response.data

async def get_by_id(db,course_id: int):
    response = db.table("courses").select("*").eq("course_id", course_id).execute()
    return response.data[0] if response.data else None

async def create(db,course: Course):
    response = db.table("courses").insert(course.model_dump()).execute()
    return response.data[0]

async def delete(db, course_id: int):
    response = db.table("courses").delete().eq("course_id", course_id).execute()
    return response.data[0] if response.data else None