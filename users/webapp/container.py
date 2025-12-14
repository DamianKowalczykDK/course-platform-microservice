from dependency_injector import containers, providers
from webapp.database.repositories.user import UserRepository
from webapp.services.users.services import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.users"
        ]
    )

    user_repository = providers.Singleton(UserRepository)

    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository
    )
