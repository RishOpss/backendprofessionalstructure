from fastapi import APIRouter

from app.api.v1.endpoints import students
from app.api.v1.endpoints import courses

api_router = APIRouter(prefix="/api")

api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])