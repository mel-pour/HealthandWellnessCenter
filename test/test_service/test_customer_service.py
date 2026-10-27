import unittest
from decimal import Decimal

from test.test_helpers import TemporaryStorageMixin
from data_access.customer_data_access import CustomerDataAccess
from services.customer_service import CustomerService


class TestCustomerService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()
        self.customer_data_access = CustomerDataAccess(self.storage)
        self.service = CustomerService(self.customer_data_access)
        self.customer = self.service.create_customer(
            1, "Milad", "1234567890", 30, "male",
            "09123456789", Decimal("100.00")
        )

    def tearDown(self):
        self.close_storage()

    def test_create_and_reload_customer(self):
        found = self.customer_data_access.find_by_id(1)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Milad")
        self.assertEqual(Decimal(str(found.balance)), Decimal("100.00"))

    def test_add_balance(self):
        self.service.add_balance(1, 50)
        self.assertEqual(Decimal(str(self.service.get_customer(1).balance)),
                         Decimal("150.00"))

    def test_deduct_balance(self):
        self.service.deduct_balance(1, 30)
        self.assertEqual(Decimal(str(self.service.get_customer(1).balance)),
                         Decimal("70.00"))

    def test_refund(self):
        self.service.refund(1, 25)
        self.assertEqual(Decimal(str(self.service.get_customer(1).balance)),
                         Decimal("125.00"))

    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.service.deduct_balance(1, 200)

    def test_duplicate_customer_id(self):
        with self.assertRaises(ValueError):
            self.service.create_customer(
                1, "Ali", "9876543210", 25, "male",
                "09111111111", Decimal("20.00")
            )

    def test_add_balance_rejects_zero(self):
        with self.assertRaises(ValueError):
            self.service.add_balance(1, 0)

    def test_add_balance_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.service.add_balance(1, -10)

    def test_deduct_balance_rejects_nan(self):
        with self.assertRaises(ValueError):
            self.service.deduct_balance(1, Decimal("NaN"))

    def test_has_enough_balance_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.service.has_enough_balance(1, -10)

if __name__ == "__main__":
    unittest.main(verbosity=2)
