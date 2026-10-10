from fastapi import APIRouter
router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
def get_courses():
    # Logic to retrieve courses from the database
    return {"message": "List of courses"}

