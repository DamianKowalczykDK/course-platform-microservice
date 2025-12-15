from dependency_injector import providers, containers
from webapp.services.auth.services import AuthService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.login"
        ]
    )
    auth_service=providers.Singleton(AuthService)

