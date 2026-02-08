from webapp.database.models.courses import Course
from webapp.services.courses.dtos import ReadCourseDTO

def to_read_dto(model: Course) -> ReadCourseDTO:
    return ReadCourseDTO(
        id=model.id,
        name=model.name,
        description=str(model.description),
        price=model.price,
        max_participants=model.max_participants,
        start_date=model.start_date,
        end_date=model.end_date
    )