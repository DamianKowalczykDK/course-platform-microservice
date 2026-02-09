from dependency_injector import containers, providers
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.services.email_service import EmailService
from webapp.services.enrolments.services import EnrolmentService
from webapp.services.invoices.services import InvoiceService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.enrolments"
        ]
    )

    enrolment_repository = providers.Singleton(EnrolmentRepository)
    email_service = providers.Singleton(EmailService)
    invoice_service = providers.Singleton(InvoiceService)

    enrolment_service = providers.Singleton(
        EnrolmentService,
        enrolment_repository=enrolment_repository,
        email_service=email_service,
        invoice_service=invoice_service,
    )