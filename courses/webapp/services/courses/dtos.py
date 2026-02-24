from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateCourseDTO:
    """
    Data Transfer Object used for creating a new course.

    Contains all required fields necessary to create a Course entity.
    The object is immutable.
    """

    name: str
    description: str
    price: float
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None


@dataclass(frozen=True)
class ReadCourseDTO:
    """
    Data Transfer Object used for returning course data.

    Represents the full course information exposed to the outside
    layers of the application. The object is immutable.
    """

    id: int
    name: str
    description: str
    price: float
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None


@dataclass(frozen=True)
class CourseIdDTO:
    """
    Data Transfer Object containing a course identifier.

    Used when an operation requires only the course ID.
    The object is immutable.
    """

    course_id: int


@dataclass(frozen=True)
class CourseNameDTO:
    """
    Data Transfer Object containing a course name.

    Used when searching or filtering courses by name.
    The object is immutable.
    """

    name: str


@dataclass(frozen=True)
class UpdateCourseDTO:
    """
    Data Transfer Object used for updating an existing course.

    Only provided (non-None) fields should be updated.
    The object is immutable.
    """

    id: int
    name: str | None = None
    description: str | None = None
    price: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = None