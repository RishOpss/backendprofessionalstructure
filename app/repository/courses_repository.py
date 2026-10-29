from supabase import Client
from schemas.course import Course

def get_all(db : Client):
    response = db.table("courses").select("*").execute()
    return response.data

def get_by_id(db : Client,course_id: int):
    response = db.table("courses").select("*").eq("course_id", course_id).execute()
    return response.data[0] if response.data else None

def create( db : Client ,course: Course ):
    response = db.table("courses").insert(course.dict()).execute()
    return response.data[0]
