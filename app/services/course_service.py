from repository import courses_repository
from schemas.course import Course

def get_courses():
    return courses_repository.get_all()

def get_course_by_id(course_id: int):
    return courses_repository.get_by_id(course_id)

def create_course(course: Course):
    return courses_repository.create(course)
