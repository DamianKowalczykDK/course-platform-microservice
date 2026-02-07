from typing import Generator, Protocol, cast
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import Session, SessionTransaction
from sqlalchemy.pool import StaticPool
from webapp.database.models.enrolments import Enrolment, Status, PaymentStatus
from webapp.extensions import db

import pytest

class _ExtensionModule(Protocol):
    db: SQLAlchemy
    migrate: Migrate


@pytest.fixture(scope="package")
def app() -> Generator[Flask, None, None]:
    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    )

    db.init_app(application)

    with application.app_context():
        db.create_all()
        yield application
        db.drop_all()
        db.engine.dispose()


@pytest.fixture()
def session(app: Flask) -> Generator[Session, None, None]:
    s: Session = cast(Session, db.session)

    s.begin_nested()

    @event.listens_for(s, "after_transaction_end")
    def _restart_nested(sess: Session, transaction: SessionTransaction) -> None:
        if transaction.nested and not getattr(transaction._parent, "nested", False):
            sess.begin_nested()

    try:
        yield s
    finally:
        s.rollback()
        event.remove(s, "after_transaction_end", _restart_nested)

@pytest.fixture()
def enrolment() -> Enrolment:
    return Enrolment(
        course_id=1,
        user_id="123",
        invoice_url="http://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING
    )

