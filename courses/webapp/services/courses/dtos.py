from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateCourseDTO:
    name: str
    description: str
    price: float
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None

@dataclass(frozen=True)
class ReadCourseDTO:
    id: int
    name: str
    description: str
    price: float
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None

@dataclass(frozen=True)
class CourseIdDTO:
    course_id: int

@dataclass(frozen=True)
class CourseNameDTO:
    name: str

@dataclass(frozen=True)
class UpdateCourseDTO:
    id: int
    name: str | None = None
    description: str | None = None
    price: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = None


