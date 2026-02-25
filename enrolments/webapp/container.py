from dependency_injector import containers, providers
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.services.email_service import EmailService
from webapp.services.enrolments.services import EnrolmentService
from webapp.services.invoices.services import InvoiceService
from concurrent.futures import ThreadPoolExecutor

class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the Enrolments microservice.

    Provides singletons for repositories, services, and external integrations,
    and wires dependencies automatically into the API package.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.enrolments"
        ]
    )

    enrolment_repository = providers.Singleton(EnrolmentRepository)
    email_service = providers.Singleton(EmailService)
    invoice_service = providers.Singleton(InvoiceService)
    executor = providers.Singleton(ThreadPoolExecutor, max_workers=2)

    enrolment_service = providers.Singleton(
        EnrolmentService,
        enrolment_repository=enrolment_repository,
        email_service=email_service,
        invoice_service=invoice_service,
        executor=executor,
    )