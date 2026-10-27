
from data_access.text_file_storage import TextFileStorage
from data_access.offering_data_access import OfferingDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess

from models.offering import Offering
from models.healthcare_center import HealthcareCenter


storage = TextFileStorage()

offering_data = OfferingDataAccess(storage)
center_data = HealthcareCenterDataAccess(storage, offering_data)

# Create and save an offering
offering = Offering(
    offering_id=10,
    name="Test Massage",
    offering_type="service",
    price=50.00,
    duration=60
)

offering_data.add(offering)
print("Offering saved!")

# Create a healthcare center containing the offering
center = HealthcareCenter(
    center_id=1,
    name="Test Healthcare Center",
    center_address="123 Test Street",
    center_phone_number="09123456789",
    offerings=[offering]
)

# Save the center
center_data.add(center)
print("Healthcare center saved!")

# Find the center
found_center = center_data.find_by_id(1)

assert found_center is not None
assert found_center.center_id == 1
assert found_center.name == "Test Healthcare Center"
assert found_center.center_address == "123 Test Street"
assert found_center.center_phone_number == "09123456789"

print("Healthcare center found successfully!")
print(found_center.get_info())

# Verify the offering relationship
assert len(found_center.offerings) == 1
assert found_center.offerings[0].offering_id == 10
assert found_center.offerings[0].name == "Test Massage"

print("Center offerings loaded successfully!")

# Load all centers
all_centers = center_data.get_all()

assert len(all_centers) >= 1

print("All healthcare centers loaded successfully!")
print("Test passed!")
