from dataclasses import dataclass

@dataclass(frozen=True)
class CreateCourseDTO:
    """
    DTO for creating a new course.

    Attributes:
        name (str): Course title.
        description (str): Course description.
        price (float): Course price.
        start_date (str): ISO formatted start date.
        end_date (str): ISO formatted end date.
        max_participants (int | None): Optional maximum number of participants.
    """
    name: str
    description: str
    price: float
    start_date: str
    end_date: str
    max_participants: int | None = None

@dataclass(frozen=True)
class CourseDTO:
    """
    DTO representing a course object returned from the service.

    Attributes:
        id (int): Unique course ID.
        name (str): Course title.
        price (float): Course price.
        description (str): Course description.
        start_date (str): ISO formatted start date.
        end_date (str): ISO formatted end date.
        max_participants (int | None): Maximum number of participants (optional).
    """
    id: int
    name: str
    price: float
    description: str
    start_date: str
    end_date: str
    max_participants: int | None = None

@dataclass(frozen=True)
class CourseIdDTO:
    """
    DTO for operations requiring only the course ID.

    Attributes:
        course_id (int): Unique course ID.
    """
    course_id: int

@dataclass(frozen=True)
class CourseNameDTO:
    """
    DTO for operations requiring only the course name.

    Attributes:
        name (str): Course title.
    """
    name: str

@dataclass(frozen=True)
class UpdateCourseDTO:
    """
    DTO for updating course information. Only provided fields will be updated.

    Attributes:
        id (int): Unique course ID.
        name (str | None): New course title (optional).
        description (str | None): New course description (optional).
        price (float | None): New course price (optional).
        start_date (str | None): New start date in ISO format (optional).
        end_date (str | None): New end date in ISO format (optional).
        max_participants (int | None): New maximum participants (optional).
    """
    id: int
    name: str | None = None
    description: str | None = None
    price: float | None = None
    start_date: str | None = None
    end_date: str | None = None
    max_participants: int | None = None