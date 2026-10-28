import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess
from models.customer import Customer


class TestCustomerDataAccess(unittest.TestCase):

    def setUp(self):
        # Create temporary storage for this test.
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "test_data.txt"

        # Initialize the expected JSON structure.
        self.file_path.write_text(
            json.dumps({
                "customers": [],
                "offerings": [],
                "appointments": [],
                "centers": []
            }),
            encoding="utf-8"
        )

        # Create storage without changing TextFileStorage itself.
        self.storage = TextFileStorage.__new__(TextFileStorage)
        self.storage.file_path = self.file_path

        self.customer_data = CustomerDataAccess(self.storage)

        self.customer = Customer(
            customer_id=1,
            name="Test Customer",
            social_id="1234567890",
            age=30,
            gender="male",
            phone_number="09128993925",
            balance=Decimal("100.00")
        )

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_add_customer(self):
        self.customer_data.add(self.customer)

        found_customer = self.customer_data.find_by_id(1)

        self.assertIsNotNone(found_customer)
        self.assertEqual(found_customer.name, "Test Customer")
        self.assertEqual(found_customer.balance, Decimal("100.00"))

    def test_get_all_customers(self):
        self.customer_data.add(self.customer)

        all_customers = self.customer_data.get_all()

        self.assertEqual(len(all_customers), 1)
        self.assertEqual(all_customers[0].customer_id, 1)

    def test_find_nonexistent_customer(self):
        found_customer = self.customer_data.find_by_id(999)

        self.assertIsNone(found_customer)

    def test_duplicate_customer_id(self):
        self.customer_data.add(self.customer)

        with self.assertRaises(ValueError):
            self.customer_data.add(self.customer)


if __name__ == "__main__":
    unittest.main()