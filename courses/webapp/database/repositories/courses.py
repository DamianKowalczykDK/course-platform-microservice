import urllib.parse

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
        stmt = select(Course).where(Course.name.ilike(name))
        return db.session.scalars(stmt).first()

    def delete_by_id(self, course_id: int) -> None:
        course = db.session.get(Course, course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
