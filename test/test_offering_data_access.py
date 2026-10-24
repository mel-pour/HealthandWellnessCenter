
from data_access.text_file_storage import TextFileStorage
from data_access.offering_data_access import OfferingDataAccess
from models.offering import Offering


storage = TextFileStorage()
offering_data = OfferingDataAccess(storage)

# Create a test offering
offering = Offering(
    offering_id=1,
    name="Relaxation Massage",
    offering_type="service",
    price=50.00,
    duration=60
)

# Save the offering
offering_data.add(offering)
print("Offering saved!")

# Find the offering
found_offering = offering_data.find_by_id(1)

assert found_offering is not None
assert found_offering.offering_id == 1
assert found_offering.name == "Relaxation Massage"
assert found_offering.price == offering.price
assert found_offering.duration == 60

print("Offering found successfully!")
print(found_offering)

# Load all offerings
all_offerings = offering_data.get_all()

assert len(all_offerings) >= 1

print("All offerings loaded successfully!")
print("Test passed!")
