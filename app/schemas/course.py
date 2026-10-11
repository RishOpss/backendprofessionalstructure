from pydantic import BaseModel, Field

class Course(BaseModel):
    course_id : int = Field(gt=0)
    name : str = Field(min_length=2,max_length=50)
    duration : int = Field(gt=0)