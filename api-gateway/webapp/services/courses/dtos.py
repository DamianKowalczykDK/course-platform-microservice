from dataclasses import dataclass

@dataclass(frozen=True)
class CreateCourseDTO:
    name: str
    description: str
    price: float
    start_date: str
    end_date: str
    max_participants: int | None = None

@dataclass(frozen=True)
class CourseDTO:
    id: int
    name: str
    price: float
    description: str
    start_date: str
    end_date: str
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
    name: str
    description: str
    price: float
    start_date: str
    end_date: str
    max_participants: int | None = None

