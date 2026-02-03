from datetime import datetime
from pydantic import BaseModel, Field

class CreateCourseSchema(BaseModel):
    name: str =  Field(min_length=2, max_length=64)
    description: str = Field(max_length=255)
    start_date: str
    end_date: str
    max_participants: int | None = Field(None, ge=0)

class CourseResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    max_participants: int | None
    start_date: str
    end_date: str

class CourseIdSchema(BaseModel):
    course_id: int

class CourseNameSchema(BaseModel):
    name: str = Field(min_length=2, max_length=64)

class UpdateCourseSchema(BaseModel):
    name: str =  Field(min_length=2, max_length=64)
    description: str = Field(max_length=255)
    start_date: str
    end_date: str
    max_participants: int | None = Field(None, ge=0)


