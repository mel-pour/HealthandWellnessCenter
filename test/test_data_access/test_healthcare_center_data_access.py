import json
import tempfile
import unittest
from pathlib import Path

from data_access.text_file_storage import TextFileStorage
from data_access.offering_data_access import OfferingDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess

from models.offering import Offering
from models.healthcare_center import HealthcareCenter


class TestHealthcareCenterDataAccess(unittest.TestCase):

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
        self.offering_data = OfferingDataAccess(self.storage)
        self.center_data = HealthcareCenterDataAccess(
            self.storage,
            self.offering_data
        )

        # Create a test offering.
        self.offering = Offering(
            offering_id=10,
            name="Test Massage",
            offering_type="service",
            price=50.00,
            duration=60
        )

        # Create a healthcare center containing the offering.
        self.center = HealthcareCenter(
            center_id=1,
            name="Test Healthcare Center",
            center_address="123 Test Street",
            center_phone_number="09123456789",
            offerings=[self.offering]
        )

    def tearDown(self):
        # Remove the temporary directory after each test.
        self.temp_directory.cleanup()

    def test_add_and_find_center(self):
        # Save the offering before saving the center.
        self.offering_data.add(self.offering)
        self.center_data.add(self.center)

        # Retrieve the center.
        found_center = self.center_data.find_by_id(1)

        # Verify the center's details.
        self.assertIsNotNone(found_center)
        self.assertEqual(found_center.center_id, 1)
        self.assertEqual(
            found_center.name,
            "Test Healthcare Center"
        )
        self.assertEqual(
            found_center.center_address,
            "123 Test Street"
        )
        self.assertEqual(
            found_center.center_phone_number,
            "09123456789"
        )

    def test_center_offerings_are_loaded(self):
        # Save the offering and center.
        self.offering_data.add(self.offering)
        self.center_data.add(self.center)

        # Retrieve the center and verify its offerings.
        found_center = self.center_data.find_by_id(1)

        self.assertIsNotNone(found_center)
        self.assertEqual(len(found_center.offerings), 1)
        self.assertEqual(
            found_center.offerings[0].offering_id,
            10
        )
        self.assertEqual(
            found_center.offerings[0].name,
            "Test Massage"
        )

    def test_get_all_centers(self):
        # Save the offering and center.
        self.offering_data.add(self.offering)
        self.center_data.add(self.center)

        # Retrieve all centers.
        all_centers = self.center_data.get_all()

        self.assertEqual(len(all_centers), 1)
        self.assertEqual(all_centers[0].center_id, 1)
        self.assertEqual(
            all_centers[0].name,
            "Test Healthcare Center"
        )


if __name__ == "__main__":
    unittest.main()