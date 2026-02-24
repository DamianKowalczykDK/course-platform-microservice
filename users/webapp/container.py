from dependency_injector import containers, providers
from webapp.database.repositories.user import UserRepository
from webapp.services.users.services import UserService
from webapp.services.email_service import EmailService

class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the Users Microservice.

    Provides singleton instances of the UserRepository, EmailService, and UserService.
    Automatically wires dependencies for the API packages.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.users"
        ]
    )

    user_repository = providers.Singleton(UserRepository)
    email_service = providers.Singleton(EmailService)

    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository,
        email_service=email_service
    )