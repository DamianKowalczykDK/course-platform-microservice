from dependency_injector import providers, containers
from webapp.services.auth.services import AuthService
from webapp.services.courses.services import CourseService
from webapp.services.enrolments.services import EnrolmentService
from webapp.services.users.services import UserService

class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container for the API Gateway.

    Provides singleton instances of all core services:
        - AuthService
        - UserService
        - CourseService
        - EnrolmentService

    Also wires these services into API packages for automatic dependency injection.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.auth",
            "webapp.api.users",
            "webapp.api.courses",
            "webapp.api.enrolments"
        ]
    )
    auth_service = providers.Singleton(AuthService)
    user_service = providers.Singleton(UserService)
    course_service = providers.Singleton(CourseService)
    enrolment_service = providers.Singleton(EnrolmentService)