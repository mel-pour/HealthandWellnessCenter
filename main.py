from repositories.text_file_storage import TextFileStorage
from repositories.customer_repository import CustomerRepository
from repositories.offering_repository import OfferingRepository
from repositories.appointment_repository import AppointmentRepository
from repositories.healthcare_center_repository import HealthcareCenterRepository

from services.customer_service import CustomerService
from services.offering_service import OfferingService
from services.appointment_service import AppointmentService
from services.healthcare_center_service import HealthcareCenterService


storage = TextFileStorage()

customer_repository = CustomerRepository(storage)
offering_repository = OfferingRepository(storage)
appointment_repository = AppointmentRepository(storage)
center_repository = HealthcareCenterRepository(storage)

customer_service = CustomerService(customer_repository)
offering_service = OfferingService(offering_repository)

appointment_service = AppointmentService(
    appointment_repository,
    customer_service,
    offering_service
)

healthcare_center_service = HealthcareCenterService(
    center_repository,
    offering_service
)