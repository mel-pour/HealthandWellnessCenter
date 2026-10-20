import unittest
from decimal import Decimal

from services.customer_service import CustomerService
from repositories.customer_repository import CustomerRepository


class TestCustomerService(unittest.TestCase):

    def setUp(self):
        self.repository = CustomerRepository()
        self.service = CustomerService(self.repository)

        self.customer = self.service.create_customer(
            1,
            "Milad",
            "1234567890",
            30,
            "male",
            "09123456789",
            Decimal("100.00")
        )

    def test_create_customer(self):
        self.assertEqual(self.customer.customer_id, 1)

    def test_add_balance(self):
        self.service.add_balance(1, 50)
        self.assertEqual(self.customer.balance, Decimal("150.00"))

    def test_deduct_balance(self):
        self.service.deduct_balance(1, 30)
        self.assertEqual(self.customer.balance, Decimal("70.00"))

    def test_refund(self):
        self.service.refund(1, 25)
        self.assertEqual(self.customer.balance, Decimal("125.00"))

    def test_find_customer(self):
        found = self.service.get_customer(1)
        self.assertIs(found, self.customer)

    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.service.deduct_balance(1, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)