from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateCourseDTO:
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None

@dataclass(frozen=True)
class ReadCourseDTO:
    id: int
    name: str
    description: str
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
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: int | None = None


