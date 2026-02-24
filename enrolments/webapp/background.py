from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from webapp.container import Container

def start_enrolment_expiration_job(app: Flask, container: Container) -> None:
    """
    Start a background job that marks expired enrolments as completed daily.

    This function:
        - Initializes a BackgroundScheduler.
        - Retrieves the EnrolmentService from the dependency injection container.
        - Defines a job that logs start and completion, and calls `expired_courses` on the service.
        - Schedules the job to run daily at midnight.
        - Starts the scheduler and logs that the background job has been started.

    Args:
        app (Flask): The Flask application instance.
        container (Container): The dependency injection container.
    """
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