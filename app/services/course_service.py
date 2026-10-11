from schemas.course import Course
from repository import courses_repository

def get_courses():
    return courses_repository.get_all()