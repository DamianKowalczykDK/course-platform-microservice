from sqlalchemy import select
from webapp.database.models.courses import Course
from webapp.database.repositories.generic import GenericRepository
from webapp.extensions import db


class CourseRepository(GenericRepository[Course]):
    """
    Repository class responsible for Course data persistence operations.

    Provides methods for retrieving and deleting Course entities
    from the database. Inherits common CRUD operations from
    GenericRepository.
    """

    def __init__(self) -> None:
        """
        Initialize the CourseRepository.

        Binds the repository to the Course model.
        """
        super().__init__(Course)

    def get_by_id(self, course_id: int) -> Course | None:
        """
        Retrieve a course by its unique identifier.

        Args:
            course_id (int): The unique identifier of the course.

        Returns:
            Course | None: The Course instance if found, otherwise None.
        """
        stmt = select(Course).where(Course.id == course_id)
        return db.session.scalars(stmt).first()

    def get_by_name(self, name: str) -> list[Course]:
        """

        Retrieve courses by name (case-insensitive, partial match).

        Args:
            name (str): Full or partial course name.

        Returns:
            list[Course]: A list of matching Course instances.
                          Returns an empty list if no courses are found.

        """
        pattern = f"%{name}%"
        stmt = select(Course).where(Course.name.ilike(pattern))
        return list(db.session.scalars(stmt).all())

    def delete_by_id(self, course_id: int) -> None:
        """
        Delete a course from the database using its ID.

        If the course exists, it is removed from the session
        and the transaction is committed.

        Args:
            course_id (int): The unique identifier of the course to delete.
        """
        course = db.session.get(Course, course_id)
        if course:
            db.session.delete(course)
            db.session.commit()