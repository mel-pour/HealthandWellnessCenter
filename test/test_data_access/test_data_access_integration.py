
from datetime import date, time
from decimal import Decimal

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess
from data_access.offering_data_access import OfferingDataAccess
from data_access.appointment_data_access import AppointmentDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess

from models.customer import Customer
from models.offering import Offering
from models.appointment import Appointment
from models.healthcare_center import HealthcareCenter


# Set up data-access classes
storage = TextFileStorage()

customer_data = CustomerDataAccess(storage)
offering_data = OfferingDataAccess(storage)
appointment_data = AppointmentDataAccess(storage)
center_data = HealthcareCenterDataAccess(storage, offering_data)


# 1. Create and save a customer
customer = Customer(
    customer_id=2,
    name="Integration Customer",
    social_id="9876543210",
    age=35,
    gender="male",
    phone_number="09120000002",
    balance=Decimal("200.00")
)

customer_data.add(customer)


# 2. Create and save an offering
offering = Offering(
    offering_id=2,
    name="Integration Massage",
    offering_type="service",
    price=75.00,
    duration=60
)

offering_data.add(offering)


# 3. Create and save an appointment
appointment = Appointment(
    appointment_id=2,
    customer_id=2,
    offering_id=2,
    appointment_date=date(2026, 12, 1),
    start_time=time(15, 0),
    price_paid=75.00,
    status="pending"
)

appointment_data.add(appointment)


# 4. Create and save a healthcare center
center = HealthcareCenter(
    center_id=2,
    name="Integration Center",
    center_address="2 Test Avenue",
    center_phone_number="09120000003",
    offerings=[offering]
)

center_data.add(center)

print("All test objects saved!")


# 5. Retrieve and verify the objects
found_customer = customer_data.find_by_id(2)
found_offering = offering_data.find_by_id(2)
found_appointment = appointment_data.find_by_id(2)
found_center = center_data.find_by_id(2)

assert found_customer is not None
assert found_customer.name == "Integration Customer"

assert found_offering is not None
assert found_offering.name == "Integration Massage"

assert found_appointment is not None
assert found_appointment.customer_id == 2
assert found_appointment.offering_id == 2

assert found_center is not None
assert found_center.name == "Integration Center"
assert len(found_center.offerings) == 1
assert found_center.offerings[0].offering_id == 2

print("All objects retrieved and verified!")


# 6. Verify persistence by loading the data again
reloaded_data = storage.load()

assert any(
    item["customer_id"] == 2
    for item in reloaded_data["customers"]
)

assert any(
    item["offering_id"] == 2
    for item in reloaded_data["offerings"]
)

assert any(
    item["appointment_id"] == 2
    for item in reloaded_data["appointments"]
)

assert any(
    item["center_id"] == 2
    for item in reloaded_data["centers"]
)

print("All records persisted in the JSON file!")
print("Integration test passed!")
