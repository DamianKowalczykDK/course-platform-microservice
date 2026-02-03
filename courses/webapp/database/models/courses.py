from webapp.extensions import db
from sqlalchemy import Integer, String, DateTime, func, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Course(db.Model): #type: ignore
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    max_participants: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),  nullable=False)

    start_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


    def __repr__(self):
        return f'Course id: {self.id} tittle: {self.name}'

    def update(
            self,
            name: str,
            description: str,
            start_date: datetime,
            end_date: datetime,
            max_participants: int | None = None
    ) -> None:
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.max_participants = max_participants



