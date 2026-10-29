from core.database import supabase
from schemas.course import Course

def get_all():
    response = supabase.table("courses").select("*").execute()
    return response.data

def get_by_id(course_id: int):
    response = supabase.table("courses").select("*").eq("course_id", course_id).execute()
    return response.data[0] if response.data else None

def create(course: Course):
    response = supabase.table("courses").insert(course.dict()).execute()
    return response.data[0]
