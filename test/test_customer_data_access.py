
from decimal import Decimal

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess


storage = TextFileStorage()
customer_data = CustomerDataAccess(storage)

# Create a test customer
from models.customer import Customer

customer = Customer(
    customer_id=1,
    name="Test Customer",
    social_id="1234567890",
    age=30,
    gender="male",
    phone_number="09128993925",
    balance=Decimal("100.00")
)

# Save the customer
customer_data.add(customer)
print("Customer saved!")

# Find the customer
found_customer = customer_data.find_by_id(1)

assert found_customer is not None
assert found_customer.name == "Test Customer"
assert found_customer.balance == Decimal("100.00")

print("Customer found successfully!")
print(found_customer.get_info())

# Load all customers
all_customers = customer_data.get_all()

assert len(all_customers) >= 1

print("All customers loaded successfully!")
print("Test passed!")
