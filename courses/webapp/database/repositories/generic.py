from flask_sqlalchemy.model import Model
from sqlalchemy import select
from webapp.extensions import db
from typing import Iterable

class GenericRepository[T: Model]:
    """
    Generic repository providing common CRUD operations.

    This class abstracts basic database interactions for a given SQLAlchemy
    model. It supports standard create, read, delete, and transaction
    management operations and is intended to be subclassed by
    entity-specific repositories.
    """

    def __init__(self, model: type[T]) -> None:
        """
        Initialize the repository with a specific SQLAlchemy model.

        Args:
            model (type[T]): The SQLAlchemy model class associated with
                             this repository.
        """
        self.model = model

    def add(self, instance: T) -> T:
        """
        Add a single instance to the current database session.

        Args:
            instance (T): The model instance to add.

        Returns:
            T: The added instance.
        """
        db.session.add(instance)
        return instance

    def add_all(self, instance: Iterable[T]) -> None:
        """
        Add multiple instances to the current database session.

        Args:
            instance (Iterable[T]): An iterable of model instances to add.
        """
        db.session.add_all(instance)

    def get(self, pk: int) -> T | None:
        """
        Retrieve an instance by its primary key.

        Args:
            pk (int): The primary key value.

        Returns:
            T | None: The retrieved instance if found, otherwise None.
        """
        return db.session.get(self.model, pk)

    def get_all(self) -> list[T]:
        """
        Retrieve all instances of the associated model.

        Returns:
            list[T]: A list of all records for the model.
        """
        stmt = select(self.model)
        return list(db.session.scalars(stmt).all())

    def delete(self, instance: T) -> None:
        """
        Mark a given instance for deletion.

        Args:
            instance (T): The model instance to delete.
        """
        db.session.delete(instance)

    def delete_by_id(self, pk: int) -> None:
        """
        Delete an instance by its primary key.

        If the object exists, it is marked for deletion.

        Args:
            pk (int): The primary key of the instance to delete.
        """
        obj = db.session.get(self.model, pk)
        if obj:
            db.session.delete(obj)

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        db.session.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        db.session.rollback()

    def flush(self) -> None:
        """
        Flush the current session.

        Sends all pending changes to the database without committing
        the transaction.
        """
        db.session.flush()

    def refresh(self, instance: T) -> None:
        """
        Refresh the state of a given instance from the database.

        Args:
            instance (T): The model instance to refresh.
        """
        db.session.refresh(instance)

    def add_and_commit(self, instance: T) -> T:
        """
        Add an instance to the session and immediately commit the transaction.

        Args:
            instance (T): The model instance to add.

        Returns:
            T: The added and committed instance.
        """
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete_and_commit(self, instance: T) -> None:
        """
        Delete an instance and immediately commit the transaction.

        Args:
            instance (T): The model instance to delete.
        """
        db.session.delete(instance)
        db.session.commit()