import unittest
from decimal import Decimal

from test.test_helpers import TemporaryStorageMixin
from data_access.offering_data_access import OfferingDataAccess
from services.offering_service import OfferingService


class TestOfferingService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()
        self.data_access = OfferingDataAccess(self.storage)
        self.service = OfferingService(self.data_access)

    def tearDown(self):
        self.close_storage()

    def test_create_and_reload_offering(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)
        found = self.service.get_offering(101)

        self.assertEqual(found.name, "Massage")
        self.assertEqual(found.price, Decimal("50.00"))
        self.assertEqual(found.duration, 60)

    def test_list_offerings(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)
        self.service.create_offering(102, "Facial", "service", 30, 30)

        self.assertEqual(len(self.service.get_all_offerings()), 2)

    def test_duplicate_offering_id(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)

        with self.assertRaises(ValueError):
            self.service.create_offering(101, "Facial", "service", 30, 30)

    def test_missing_offering(self):
        with self.assertRaises(ValueError):
            self.service.get_offering(999)

    def test_update_offering(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)

        updated = self.service.update_offering(
            101, "Deep Tissue Massage", "service", 65, 90
        )

        self.assertEqual(updated.name, "Deep Tissue Massage")
        self.assertEqual(updated.price, Decimal("65.00"))
        self.assertEqual(updated.duration, 90)

        # Confirm the changes were persisted.
        reloaded = self.service.get_offering(101)
        self.assertEqual(reloaded.name, "Deep Tissue Massage")
        self.assertEqual(reloaded.price, Decimal("65.00"))
        self.assertEqual(reloaded.duration, 90)

    def test_update_missing_offering(self):
        with self.assertRaises(ValueError):
            self.service.update_offering(
                999, "Massage", "service", 50, 60
            )

    def test_create_offering_rejects_invalid_price(self):
        with self.assertRaises(ValueError):
            self.service.create_offering(
                101, "Massage", "service", Decimal("NaN"), 60
            )

    def test_create_offering_rejects_boolean_price(self):
        with self.assertRaises(ValueError):
            self.service.create_offering(
                101, "Massage", "service", True, 60
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)