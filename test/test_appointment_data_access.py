
from datetime import date, time

from data_access.text_file_storage import TextFileStorage
from data_access.appointment_data_access import AppointmentDataAccess
from models.appointment import Appointment


storage = TextFileStorage()
appointment_data = AppointmentDataAccess(storage)

# Create a test appointment
appointment = Appointment(
    appointment_id=1,
    customer_id=1,
    offering_id=1,
    appointment_date=date(2026, 11, 15),
    start_time=time(14, 30),
    price_paid=50.00,
    status="pending"
)

# Save the appointment
appointment_data.add(appointment)
print("Appointment saved!")

# Find the appointment
found_appointment = appointment_data.find_by_id(1)

assert found_appointment is not None
assert found_appointment.appointment_id == 1
assert found_appointment.customer_id == 1
assert found_appointment.offering_id == 1
assert found_appointment.appointment_date == date(2026, 11, 15)
assert found_appointment.start_time == time(14, 30)
assert found_appointment.price_paid == appointment.price_paid
assert found_appointment.status == "pending"

print("Appointment found successfully!")
print(found_appointment)

# Load all appointments
all_appointments = appointment_data.get_all()

assert len(all_appointments) >= 1

print("All appointments loaded successfully!")
print("Test passed!")
