import unittest

from test.test_helpers import TemporaryStorageMixin
from repositories.offering_repository import OfferingRepository
from services.offering_service import OfferingService


class TestOfferingService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()
        self.repository = OfferingRepository(self.storage)
        self.service = OfferingService(self.repository)

    def tearDown(self):
        self.close_storage()

    def test_create_and_reload_offering(self):
        self.service.create_offering(101, "Massage", "service", 50, 60)
        found = self.service.get_offering(101)
        self.assertEqual(found.name, "Massage")
        self.assertEqual(float(found.price), 50.0)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
