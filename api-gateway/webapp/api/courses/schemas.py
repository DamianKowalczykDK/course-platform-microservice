from pydantic import BaseModel, Field

class CreateCourseSchema(BaseModel):
    """
    Schema for creating a new course.

    Fields:
        name (str): Course name, 2-64 characters.
        description (str): Course description, max 255 characters.
        price (float): Price of the course.
        start_date (str): Start date in ISO format.
        end_date (str): End date in ISO format.
        max_participants (int | None): Optional maximum number of participants (>= 0).
    """
    name: str = Field(min_length=2, max_length=64)
    description: str = Field(max_length=255)
    price: float
    start_date: str
    end_date: str
    max_participants: int | None = Field(None, ge=0)


class CourseResponseSchema(BaseModel):
    """
    Schema representing a course response.

    Fields:
        id (int): Course ID.
        name (str): Course name.
        description (str): Course description.
        price (float): Course price.
        max_participants (int | None): Maximum number of participants (optional).
        start_date (str): Start date in ISO format.
        end_date (str): End date in ISO format.
    """
    id: int
    name: str
    description: str
    price: float
    max_participants: int | None
    start_date: str
    end_date: str

class CoursesListResponseSchema(BaseModel):
    """
       Schema representing a list of courses returned by the API.

       Attributes:
           courses (list[CourseResponseSchema]): List of course objects. Can be empty if no courses match the query.
       """
    courses: list[CourseResponseSchema]


class CourseIdSchema(BaseModel):
    """
    Schema for operations that require a course ID.

    Fields:
        course_id (int): The ID of the course.
    """
    course_id: int


class CourseNameSchema(BaseModel):
    """
    Schema for operations that require a course name.

    Fields:
        name (str): Course name, 2-64 characters.
    """
    name: str = Field(min_length=2, max_length=64)


class UpdateCourseSchema(BaseModel):
    """
    Schema for updating a course. All fields are optional; only provided fields will be updated.

    Fields:
        name (str | None): Updated course name, 2-64 characters.
        description (str | None): Updated course description, max 255 characters.
        price (float | None): Updated course price.
        start_date (str | None): Updated start date in ISO format.
        end_date (str | None): Updated end date in ISO format.
        max_participants (int | None): Updated max participants (>= 0, optional).
    """
    name: str | None = Field(None, min_length=2, max_length=64)
    description: str | None = Field(None, max_length=255)
    price: float | None = None
    start_date: str | None = None
    end_date: str | None = None
    max_participants: int | None = Field(None, ge=0)