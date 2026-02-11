from dependency_injector import providers, containers
from webapp.services.auth.services import AuthService
from webapp.services.courses.services import CourseService
from webapp.services.enrolments.services import EnrolmentService
from webapp.services.users.services import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.auth",
            "webapp.api.users",
            "webapp.api.courses",
            "webapp.api.enrolments"

        ]
    )
    auth_service=providers.Singleton(AuthService)
    user_service=providers.Singleton(UserService)
    course_service=providers.Singleton(CourseService)
    enrolment_service=providers.Singleton(EnrolmentService)

