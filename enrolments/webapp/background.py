from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from webapp.container import Container


def start_enrolment_expiration_job(app: Flask, container: Container) -> None:
    scheduler = BackgroundScheduler()
    enrolment_service = container.enrolment_service()

    def job() -> None:
        with app.app_context():
            app.logger.info("Running enrolment expiration job")
            enrolment_service.expired_courses()
            app.logger.info("Finished enrolment expiration job")

    scheduler.add_job(job, 'cron', hour=0, minute=0)
    scheduler.start()

    app.logger.info("Background job started ...")

