from typing import Iterable
from sqlalchemy import select
from flask_sqlalchemy.model import Model
from webapp.extensions import db

class GenericRepository[T: Model]:
    """
    A generic repository providing basic CRUD operations for SQLAlchemy models.

    Attributes:
        model (type[T]): The SQLAlchemy model class managed by this repository.
    """

    def __init__(self, model: type[T]) -> None:
        """
        Initialize the repository with the given model class.

        Args:
            model (type[T]): The SQLAlchemy model class.
        """
        self.model = model

    def add(self, instance: T) -> T:
        """
        Add an instance to the current session without committing.

        Args:
            instance (T): The instance to add.

        Returns:
            T: The added instance.
        """
        db.session.add(instance)
        return instance

    def add_all(self, instance: Iterable[T]) -> None:
        """
        Add multiple instances to the session without committing.

        Args:
            instance (Iterable[T]): Collection of instances to add.
        """
        db.session.add_all(instance)

    def get(self, pk: int) -> T | None:
        """
        Retrieve an instance by its primary key.

        Args:
            pk (int): Primary key of the instance.

        Returns:
            T | None: The instance if found, otherwise None.
        """
        return db.session.get(self.model, pk)

    def get_all(self) -> list[T]:
        """
        Retrieve all instances of the model.

        Returns:
            list[T]: List of all model instances.
        """
        stmt = select(self.model)
        return list(db.session.scalars(stmt).all())

    def delete(self, instance: T) -> None:
        """
        Delete an instance from the session.

        Args:
            instance (T): The instance to delete.
        """
        db.session.delete(instance)

    def delete_by_id(self, pk: int) -> None:
        """
        Delete an instance by primary key.

        Args:
            pk (int): Primary key of the instance.
        """
        obj = db.session.get(self.model, pk)
        if obj:
            db.session.delete(obj)

    def commit(self) -> None:
        """Commit the current session."""
        db.session.commit()

    def rollback(self) -> None:
        """Rollback the current session."""
        db.session.rollback()

    def flush(self) -> None:
        """Flush the session (push changes to DB without committing)."""
        db.session.flush()

    def refresh(self, instance: T) -> None:
        """
        Refresh the state of an instance from the database.

        Args:
            instance (T): The instance to refresh.
        """
        db.session.refresh(instance)

    def add_and_commit(self, instance: T) -> T:
        """
        Add an instance to the session and commit immediately.

        Args:
            instance (T): The instance to add.

        Returns:
            T: The added instance.
        """
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete_and_commit(self, instance: T) -> None:
        """
        Delete an instance from the session and commit immediately.

        Args:
            instance (T): The instance to delete.
        """
        db.session.delete(instance)
        db.session.commit()