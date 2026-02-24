from dependency_injector import containers, providers
from webapp.database.repositories.courses import CourseRepository
from webapp.services.courses.services import CourseService


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container configuration.

    Defines application-level dependencies and their lifecycle.
    Registers repositories and services as singletons and configures
    wiring for selected packages.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.courses"
        ]
    )

    course_repository = providers.Singleton(CourseRepository)

    courses_service = providers.Singleton(
        CourseService,
        course_repository=course_repository
    )