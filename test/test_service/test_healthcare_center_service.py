import unittest

from test.test_helpers import TemporaryStorageMixin
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
from data_access.offering_data_access import OfferingDataAccess
from services.offering_service import OfferingService
from services.healthcare_center_service import HealthcareCenterService


class TestHealthcareCenterService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()

        self.offering_data_access = OfferingDataAccess(self.storage)
        self.healthcare_center_data_access = HealthcareCenterDataAccess(
            self.storage,
            self.offering_data_access
        )

        self.offering_service = OfferingService(
            self.offering_data_access
        )

        self.service = HealthcareCenterService(
            self.healthcare_center_data_access,
            self.offering_service
        )

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
        self.offering_service.create_offering(
            101, "Massage", "service", 50, 60
        )

        offerings = self.offering_service.get_all_offerings()

        self.assertEqual(len(offerings), 1)
        self.assertEqual(offerings[0].name, "Massage")

    def test_update_center(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )

        updated = self.service.update_center(
            1, "Premium Wellness Center", "Karaj", "09111111111"
        )

        self.assertEqual(updated.name, "Premium Wellness Center")
        self.assertEqual(updated.center_address, "Karaj")
        self.assertEqual(updated.center_phone_number, "09111111111")

        # Verify that the changes were persisted.
        reloaded = self.service.get_center(1)

        self.assertEqual(reloaded.name, "Premium Wellness Center")
        self.assertEqual(reloaded.center_address, "Karaj")

    def test_update_missing_center(self):
        with self.assertRaises(ValueError):
            self.service.update_center(
                999, "Wellness Center", "Tehran", "09123456789"
            )

    def test_add_offering_to_center(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )

        self.offering_service.create_offering(
            101, "Massage", "service", 50, 60
        )

        updated_center = self.service.add_offering_to_center(1, 101)

        self.assertEqual(len(updated_center.offerings), 1)
        self.assertEqual(updated_center.offerings[0].offering_id, 101)

        # Verify that the association was persisted.
        reloaded = self.service.get_center(1)

        self.assertEqual(len(reloaded.offerings), 1)
        self.assertEqual(reloaded.offerings[0].name, "Massage")

    def test_add_duplicate_offering_to_center(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )

        self.offering_service.create_offering(
            101, "Massage", "service", 50, 60
        )

        self.service.add_offering_to_center(1, 101)

        with self.assertRaises(ValueError):
            self.service.add_offering_to_center(1, 101)

        # The offering should appear only once.
        center = self.service.get_center(1)
        self.assertEqual(len(center.offerings), 1)

    def test_add_missing_offering_to_center(self):
        self.service.create_center(
            1, "Wellness Center", "Tehran", "09123456789"
        )

        with self.assertRaises(ValueError):
            self.service.add_offering_to_center(1, 999)

        self.assertEqual(len(self.service.get_center(1).offerings), 0)

    def test_add_offering_to_missing_center(self):
        self.offering_service.create_offering(
            101, "Massage", "service", 50, 60
        )

        with self.assertRaises(ValueError):
            self.service.add_offering_to_center(999, 101)


if __name__ == "__main__":
    unittest.main(verbosity=2)