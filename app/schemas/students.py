from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="The name of the student")
    age: int = Field(..., ge=16, le=60, description="The age of the student")
    course_id: str = Field(..., description="The ID of the course")
    
class StudentUpdate(BaseModel):
    name: str = Field( min_length=3, max_length=50, description="The name of the student")
    age: int = Field( ge=16, le=60, description="The age of the student")
    course_id: str = Field( description="The ID of the course")