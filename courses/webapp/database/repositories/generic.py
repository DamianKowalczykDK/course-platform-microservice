from typing import Iterable
from sqlalchemy import select
from flask_sqlalchemy.model import Model
from webapp.extensions import db

class GenericRepository[T: Model]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    def add(self, instance: T) -> T:
        db.session.add(instance)
        return instance

    def add_all(self, instance: Iterable[T]) -> None:
        db.session.add_all(instance)

    def get(self, pk: int) -> T | None:
        return db.session.get(self.model, pk)

    def get_all(self) -> list[T]:
        stmt = select(self.model)
        return list(db.session.scalars(stmt).all())

    def delete(self, instance: T) -> None:
        db.session.delete(instance)

    def delete_by_id(self, pk: int) -> None:
        obj = db.session.get(self.model, pk)
        if obj:
            db.session.delete(obj)

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rollback()

    def flush(self) -> None:
        db.session.flush()

    def refresh(self, instance: T) -> None:
        db.session.refresh(instance)

    def add_and_commit(self, instance: T) -> T:
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete_and_commit(self, instance: T) -> None:
        db.session.delete(instance)
        db.session.commit()




