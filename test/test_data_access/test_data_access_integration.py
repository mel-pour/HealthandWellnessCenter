import json
import tempfile
import unittest
from datetime import date, time
from decimal import Decimal
from pathlib import Path

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess
from data_access.offering_data_access import OfferingDataAccess
from data_access.appointment_data_access import AppointmentDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess

from models.customer import Customer
from models.offering import Offering
from models.appointment import Appointment
from models.healthcare_center import HealthcareCenter


class TestDataAccessIntegration(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test data.
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "test_data.txt"

        # Initialize an empty JSON file.
        self.file_path.write_text(
            json.dumps({
                "customers": [],
                "offerings": [],
                "appointments": [],
                "centers": []
            }),
            encoding="utf-8"
        )

        # Use the temporary file instead of the real data file.
        self.storage = TextFileStorage.__new__(TextFileStorage)
        self.storage.file_path = self.file_path

        # Set up data-access classes.
        self.customer_data = CustomerDataAccess(self.storage)
        self.offering_data = OfferingDataAccess(self.storage)
        self.appointment_data = AppointmentDataAccess(self.storage)
        self.center_data = HealthcareCenterDataAccess(
            self.storage,
            self.offering_data
        )

        # Create test objects.
        self.customer = Customer(
            customer_id=2,
            name="Integration Customer",
            social_id="9876543210",
            age=35,
            gender="male",
            phone_number="09120000002",
            balance=Decimal("200.00")
        )

        self.offering = Offering(
            offering_id=2,
            name="Integration Massage",
            offering_type="service",
            price=75.00,
            duration=60
        )

        self.appointment = Appointment(
            appointment_id=2,
            customer_id=2,
            offering_id=2,
            appointment_date=date(2026, 12, 1),
            start_time=time(15, 0),
            price_paid=75.00,
            status="pending"
        )

        self.center = HealthcareCenter(
            center_id=2,
            name="Integration Center",
            center_address="2 Test Avenue",
            center_phone_number="09120000003",
            offerings=[self.offering]
        )

    def tearDown(self):
        # Remove the temporary directory after each test.
        self.temp_directory.cleanup()

    def save_all_objects(self):
        """Save all objects and their relationships."""
        self.customer_data.add(self.customer)
        self.offering_data.add(self.offering)
        self.appointment_data.add(self.appointment)
        self.center_data.add(self.center)

    def test_save_and_retrieve_all_objects(self):
        # Save all objects.
        self.save_all_objects()

        # Retrieve the objects.
        found_customer = self.customer_data.find_by_id(2)
        found_offering = self.offering_data.find_by_id(2)
        found_appointment = self.appointment_data.find_by_id(2)
        found_center = self.center_data.find_by_id(2)

        # Verify the customer.
        self.assertIsNotNone(found_customer)
        self.assertEqual(
            found_customer.name,
            "Integration Customer"
        )

        # Verify the offering.
        self.assertIsNotNone(found_offering)
        self.assertEqual(
            found_offering.name,
            "Integration Massage"
        )

        # Verify the appointment.
        self.assertIsNotNone(found_appointment)
        self.assertEqual(found_appointment.customer_id, 2)
        self.assertEqual(found_appointment.offering_id, 2)

        # Verify the healthcare center and its offering relationship.
        self.assertIsNotNone(found_center)
        self.assertEqual(found_center.name, "Integration Center")
        self.assertEqual(len(found_center.offerings), 1)
        self.assertEqual(
            found_center.offerings[0].offering_id,
            2
        )

    def test_all_objects_are_persisted(self):
        # Save all objects.
        self.save_all_objects()

        # Reload the data from the JSON file.
        reloaded_data = self.storage.load()

        # Verify that all four object types were persisted.
        self.assertTrue(
            any(
                item["customer_id"] == 2
                for item in reloaded_data["customers"]
            )
        )

        self.assertTrue(
            any(
                item["offering_id"] == 2
                for item in reloaded_data["offerings"]
            )
        )

        self.assertTrue(
            any(
                item["appointment_id"] == 2
                for item in reloaded_data["appointments"]
            )
        )

        self.assertTrue(
            any(
                item["center_id"] == 2
                for item in reloaded_data["centers"]
            )
        )


if __name__ == "__main__":
    unittest.main()