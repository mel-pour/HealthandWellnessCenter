import tkinter as tk

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess

from services.customer_service import CustomerService

from controllers.customer_controller import CustomerController

from views.main_view import MainView


def main():
    # Data access
    storage = TextFileStorage()
    customer_data_access = CustomerDataAccess(storage)

    # Service
    customer_service = CustomerService(customer_data_access)

    # Controller
    customer_controller = CustomerController(customer_service)

    # View
    root = tk.Tk()
    MainView(root, customer_controller)

    root.mainloop()


if __name__ == "__main__":
    main()









# from data_access.text_file_storage import TextFileStorage
# from data_access.customer_data_access import CustomerDataAccess
# from data_access.offering_data_access import OfferingDataAccess
# from data_access.appointment_data_access import AppointmentDataAccess
# from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
#
# from services.customer_service import CustomerService
# from services.offering_service import OfferingService
# from services.appointment_service import AppointmentService
# from services.healthcare_center_service import HealthcareCenterService
#
# from controllers.customer_controller import CustomerController
# from controllers.offering_controller import OfferingController
# from controllers.appointment_controller import AppointmentController
# from controllers.healthcare_center_controller import HealthcareCenterController
#
# storage = TextFileStorage()
#
# customer_data_access = CustomerDataAccess(storage)
# offering_data_access = OfferingDataAccess(storage)
# appointment_data_access = AppointmentDataAccess(storage)
#
# center_data_access = HealthcareCenterDataAccess(
#     storage,
#     offering_data_access
# )
#
# customer_service = CustomerService(customer_data_access)
# offering_service = OfferingService(offering_data_access)
#
# appointment_service = AppointmentService(
#     appointment_data_access,
#     customer_service,
#     offering_service
# )
#
# healthcare_center_service = HealthcareCenterService(
#     center_data_access,
#     offering_service
# )
#
# customer_controller = CustomerController(customer_service)
# offering_controller = OfferingController(offering_service)
# appointment_controller = AppointmentController(appointment_service)
# healthcare_center_controller = HealthcareCenterController(
#     healthcare_center_service
# )

# python -m unittest discover -s test -p "test_*.py" -v

