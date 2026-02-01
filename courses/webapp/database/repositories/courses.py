from sqlalchemy import select
from webapp.database.models.courses import Course
from webapp.database.repositories.generic import GenericRepository
from webapp.extensions import db


class CourseRepository(GenericRepository[Course]):
    def __init__(self) -> None:
        super().__init__(Course)

    def get_by_id(self, course_id: int) -> Course | None:
        stmt = select(Course).where(Course.id == course_id)
        return db.session.scalars(stmt).first()

    def get_by_name(self, name: str) -> Course | None:
        stmt = select(Course).where(Course.name == name)
        return db.session.scalars(stmt).first()

    def delete_by_id(self, course_id: int) -> None:
        stmt = select(Course).where(Course.id == course_id)
        db.session.delete(stmt)
