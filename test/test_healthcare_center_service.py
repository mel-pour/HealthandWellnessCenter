import unittest

from test.test_helpers import TemporaryStorageMixin
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
from data_access.offering_data_access import OfferingDataAccess
from services.offering_service import OfferingService
from services.healthcare_center_service import HealthcareCenterService


class TestHealthcareCenterService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()
        self.healthcare_center_data_access = HealthcareCenterDataAccess(self.storage)
        self.offering_service = OfferingService(OfferingDataAccess(self.storage))
        self.service = HealthcareCenterService(self.healthcare_center_data_access, self.offering_service)

    def tearDown(self):
        self.close_storage()

    def test_create_and_reload_center(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )
        found = self.service.get_center(1)
        self.assertEqual(found.name, "Wellness Center")
        self.assertEqual(found.center_address, "Tehran")

    def test_duplicate_center_id(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )
        with self.assertRaises(ValueError):
            self.service.create_center(
                1, "Health Center", "Karaj", "09111111111"
            )

    def test_center_can_list_offerings(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)
        offerings = self.service.get_all_offerings()
        self.assertEqual(len(offerings), 1)
        self.assertEqual(offerings[0].name, "Massage")


if __name__ == "__main__":
    unittest.main(verbosity=2)
