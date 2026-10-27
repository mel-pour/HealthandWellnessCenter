import unittest
from unittest.mock import Mock

from controllers.offering_controller import OfferingController


class TestOfferingController(unittest.TestCase):

    def setUp(self):
        self.offering_service = Mock()
        self.controller = OfferingController(self.offering_service)

    def test_create_offering_success(self):
        expected_offering = Mock()
        self.offering_service.create_offering.return_value = expected_offering

        result = self.controller.create_offering(
            "O001", "Massage", "Healthcare", 50, 60
        )

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Offering created successfully.")
        self.assertIs(result[2], expected_offering)

    def test_create_offering_validation_error(self):
        self.offering_service.create_offering.side_effect = ValueError(
            "Invalid offering ID."
        )

        result = self.controller.create_offering(
            "O001", "Massage", "Healthcare", 50, 60
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Invalid offering ID.")
        self.assertIsNone(result[2])

    def test_create_offering_unexpected_error(self):
        self.offering_service.create_offering.side_effect = RuntimeError(
            "Unexpected problem."
        )

        result = self.controller.create_offering(
            "O001", "Massage", "Healthcare", 50, 60
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "An unexpected error occurred.")
        self.assertIsNone(result[2])

    def test_get_offering_success(self):
        expected_offering = Mock()
        self.offering_service.get_offering.return_value = expected_offering

        result = self.controller.get_offering("O001")

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Offering found successfully.")
        self.assertIs(result[2], expected_offering)
        self.offering_service.get_offering.assert_called_once_with("O001")

    def test_get_offering_not_found(self):
        self.offering_service.get_offering.side_effect = ValueError(
            "Offering not found."
        )

        result = self.controller.get_offering("O999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Offering not found.")
        self.assertIsNone(result[2])

    def test_get_all_offerings_success(self):
        expected_offerings = [Mock(), Mock()]
        self.offering_service.get_all_offerings.return_value = expected_offerings

        result = self.controller.get_all_offerings()

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Offerings retrieved successfully.")
        self.assertIs(result[2], expected_offerings)

    def test_get_all_offerings_unexpected_error(self):
        self.offering_service.get_all_offerings.side_effect = RuntimeError(
            "Storage problem."
        )

        result = self.controller.get_all_offerings()

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Could not retrieve offerings.")
        self.assertIsNone(result[2])

    def test_update_offering_success(self):
        expected_offering = Mock()
        self.offering_service.update_offering.return_value = expected_offering

        result = self.controller.update_offering(
            "O001", "Deep Tissue Massage", "Healthcare", 65, 60
        )

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Offering updated successfully.")
        self.assertIs(result[2], expected_offering)

        self.offering_service.update_offering.assert_called_once_with(
            "O001", "Deep Tissue Massage", "Healthcare", 65, 60
        )

    def test_update_offering_validation_error(self):
        self.offering_service.update_offering.side_effect = ValueError(
            "Invalid price."
        )

        result = self.controller.update_offering(
            "O001", "Massage", "Healthcare", -10, 60
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Invalid price.")
        self.assertIsNone(result[2])

    def test_update_offering_unexpected_error(self):
        self.offering_service.update_offering.side_effect = RuntimeError(
            "Unexpected problem."
        )

        result = self.controller.update_offering(
            "O001", "Massage", "Healthcare", 50, 60
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "An unexpected error occurred.")
        self.assertIsNone(result[2])

    def test_get_offering_info_success(self):
        expected_info = "ID: O001\nName: Massage"
        self.offering_service.get_offering_info.return_value = expected_info

        result = self.controller.get_offering_info("O001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Offering information retrieved successfully."
        )
        self.assertEqual(result[2], expected_info)

    def test_get_offering_info_validation_error(self):
        self.offering_service.get_offering_info.side_effect = ValueError(
            "Offering not found."
        )

        result = self.controller.get_offering_info("O999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Offering not found.")
        self.assertIsNone(result[2])


if __name__ == "__main__":
    unittest.main()