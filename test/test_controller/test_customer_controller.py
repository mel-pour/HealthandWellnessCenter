import unittest
from unittest.mock import Mock

from controllers.customer_controller import CustomerController


class TestCustomerController(unittest.TestCase):

    def setUp(self):
        self.customer_service = Mock()
        self.controller = CustomerController(self.customer_service)

    def test_create_customer_success(self):
        expected_customer = Mock()
        self.customer_service.create_customer.return_value = expected_customer

        result = self.controller.create_customer(
            "C001", "John", "123456", 30, "Male", "5551234", 100
        )

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], "Customer created successfully.")
        self.assertIs(result[2], expected_customer)

    def test_create_customer_validation_error(self):
        self.customer_service.create_customer.side_effect = ValueError(
            "Invalid customer ID."
        )

        result = self.controller.create_customer(
            "C001", "John", "123456", 30, "Male", "5551234", 100
        )

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Invalid customer ID.")
        self.assertIsNone(result[2])

    def test_create_customer_unexpected_error(self):
        self.customer_service.create_customer.side_effect = RuntimeError(
            "Unexpected problem."
        )

        result = self.controller.create_customer(
            "C001", "John", "123456", 30, "Male", "5551234", 100
        )

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "An unexpected error occurred.")
        self.assertIsNone(result[2])

    def test_get_customer_success(self):
        expected_customer = Mock()
        self.customer_service.get_customer.return_value = expected_customer

        result = self.controller.get_customer("C001")

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Customer found successfully.")
        self.assertIs(result[2], expected_customer)
        self.customer_service.get_customer.assert_called_once_with("C001")

    def test_get_customer_not_found(self):
        self.customer_service.get_customer.side_effect = ValueError(
            "Customer not found."
        )

        result = self.controller.get_customer("C999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Customer not found.")
        self.assertIsNone(result[2])

    def test_get_all_customers_success(self):
        expected_customers = [Mock(), Mock()]
        self.customer_service.get_all_customers.return_value = expected_customers

        result = self.controller.get_all_customers()

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Customers retrieved successfully.")
        self.assertIs(result[2], expected_customers)

    def test_get_all_customers_unexpected_error(self):
        self.customer_service.get_all_customers.side_effect = RuntimeError(
            "Storage problem."
        )

        result = self.controller.get_all_customers()

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Could not retrieve customers.")
        self.assertIsNone(result[2])

    def test_get_customer_info_success(self):
        expected_info = "ID: C001\nName: John"
        self.customer_service.get_customer_info.return_value = expected_info

        result = self.controller.get_customer_info("C001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Customer information retrieved successfully."
        )
        self.assertEqual(result[2], expected_info)

    def test_add_balance_success(self):
        expected_customer = Mock()
        self.customer_service.get_customer.return_value = expected_customer

        result = self.controller.add_balance("C001", 50)

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Balance added successfully.")
        self.assertIs(result[2], expected_customer)
        self.customer_service.add_balance.assert_called_once_with("C001", 50)

    def test_add_balance_error(self):
        self.customer_service.add_balance.side_effect = ValueError(
            "Amount must be positive."
        )

        result = self.controller.add_balance("C001", -50)

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Amount must be positive.")
        self.assertIsNone(result[2])

    def test_has_enough_balance_true(self):
        self.customer_service.has_enough_balance.return_value = True

        result = self.controller.has_enough_balance("C001", 50)

        self.assertEqual(
            result, (True, "Sufficient balance.", True)
        )

    def test_has_enough_balance_false(self):
        self.customer_service.has_enough_balance.return_value = False

        result = self.controller.has_enough_balance("C001", 500)

        self.assertEqual(
            result, (True, "Insufficient account balance.", False)
        )

    def test_deduct_balance_success(self):
        expected_customer = Mock()
        self.customer_service.get_customer.return_value = expected_customer

        result = self.controller.deduct_balance("C001", 25)

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Balance deducted successfully.")
        self.assertIs(result[2], expected_customer)
        self.customer_service.deduct_balance.assert_called_once_with(
            "C001", 25
        )

    def test_refund_success(self):
        expected_customer = Mock()
        self.customer_service.get_customer.return_value = expected_customer

        result = self.controller.refund("C001", 20)

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Refund processed successfully.")
        self.assertIs(result[2], expected_customer)
        self.customer_service.refund.assert_called_once_with("C001", 20)


if __name__ == "__main__":
    unittest.main()
