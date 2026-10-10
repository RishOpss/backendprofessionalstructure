from fastapi import APIRouter

from api.endpoints import students, courses

api_router = APIRouter(prefix="/api")

api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])