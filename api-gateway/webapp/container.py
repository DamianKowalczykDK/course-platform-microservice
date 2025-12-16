from dependency_injector import providers, containers
from webapp.services.auth.services import AuthService
from webapp.services.users.services import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.login",
            "webapp.api.users"
        ]
    )
    auth_service=providers.Singleton(AuthService)
    user_service=providers.Singleton(UserService)

