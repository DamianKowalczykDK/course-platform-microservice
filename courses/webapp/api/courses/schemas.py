from datetime import datetime
from pydantic import BaseModel, Field


class CreateCourseSchema(BaseModel):
    """
    Schema for creating a new course via API request.

    Attributes:
        name (str): Name of the course (2–64 characters).
        description (str): Description of the course (max 255 characters).
        price (float): Price of the course (must be >= 0).
        start_date (datetime): Start date and time of the course.
        end_date (datetime): End date and time of the course.
        max_participants (int | None): Optional maximum number of participants (>= 0).
    """
    name: str = Field(min_length=2, max_length=64)
    description: str = Field(max_length=255)
    price: float = Field(ge=0)
    start_date: datetime
    end_date: datetime
    max_participants: int | None = Field(None, ge=0)


class CourseResponseSchema(BaseModel):
    """
    Schema representing course data in API responses.

    Attributes:
        id (int): Unique identifier of the course.
        name (str): Name of the course.
        description (str): Description of the course.
        price (float): Price of the course.
        max_participants (int | None): Maximum number of participants, if set.
        start_date (datetime): Start date and time of the course.
        end_date (datetime): End date and time of the course.
    """
    id: int
    name: str
    description: str
    price: float
    max_participants: int | None
    start_date: datetime
    end_date: datetime


class CourseIdSchema(BaseModel):
    """
    Schema for operations requiring a course ID.

    Attributes:
        course_id (int): Unique identifier of the course.
    """
    course_id: int


class CourseNameSchema(BaseModel):
    """
    Schema for operations requiring a course name.

    Attributes:
        name (str): Name of the course (2–64 characters).
    """
    name: str = Field(min_length=2, max_length=64)


class UpdateCourseSchema(BaseModel):
    """
    Schema for updating an existing course via API request.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name (str | None): Name of the course (2–64 characters).
        description (str | None): Description of the course (max 255 characters).
        price (float | None): Price of the course (must be >= 0 if provided).
        start_date (datetime | None): Start date and time of the course.
        end_date (datetime | None): End date and time of the course.
        max_participants (int | None): Maximum number of participants (>= 0 if provided).
    """
    name: str | None = Field(None, min_length=2, max_length=64)
    description: str | None = Field(None, max_length=255)
    price: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = Field(None, ge=0)