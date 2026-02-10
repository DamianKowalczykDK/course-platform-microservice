from datetime import datetime
from pydantic import BaseModel, Field

class CreateCourseSchema(BaseModel):
    name: str =  Field(min_length=2, max_length=64)
    description: str = Field(max_length=255)
    price: float = Field(ge=0)
    start_date: datetime
    end_date: datetime
    max_participants: int | None = Field(None, ge=0)


class CourseResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    max_participants: int | None
    start_date: datetime
    end_date: datetime

class CourseIdSchema(BaseModel):
    course_id: int

class CourseNameSchema(BaseModel):
    name: str = Field(min_length=2, max_length=64)

class UpdateCourseSchema(BaseModel):
    name: str | None =  Field(None, min_length=2, max_length=64)
    description: str | None = Field(None, max_length=255)
    price: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = Field(None, ge=0)


