import unittest
from unittest.mock import Mock

from controllers.healthcare_center_controller import HealthcareCenterController


class TestHealthcareCenterController(unittest.TestCase):

    def setUp(self):
        self.healthcare_center_service = Mock()
        self.controller = HealthcareCenterController(
            self.healthcare_center_service
        )

    def test_create_center_success(self):
        expected_center = Mock()
        self.healthcare_center_service.create_center.return_value = (
            expected_center
        )

        result = self.controller.create_center(
            "HC001", "Wellness Center", "Main Street 1", "5551234"
        )

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Healthcare center created successfully."
        )
        self.assertIs(result[2], expected_center)

    def test_create_center_validation_error(self):
        self.healthcare_center_service.create_center.side_effect = ValueError(
            "Invalid center ID."
        )

        result = self.controller.create_center(
            "HC001", "Wellness Center", "Main Street 1", "5551234"
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Invalid center ID.")
        self.assertIsNone(result[2])

    def test_get_center_success(self):
        expected_center = Mock()
        self.healthcare_center_service.get_center.return_value = (
            expected_center
        )

        result = self.controller.get_center("HC001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Healthcare center found successfully."
        )
        self.assertIs(result[2], expected_center)

    def test_get_center_not_found(self):
        self.healthcare_center_service.get_center.side_effect = ValueError(
            "Healthcare center not found."
        )

        result = self.controller.get_center("HC999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Healthcare center not found.")
        self.assertIsNone(result[2])

    def test_get_all_centers_success(self):
        expected_centers = [Mock(), Mock()]
        self.healthcare_center_service.get_all_centers.return_value = (
            expected_centers
        )

        result = self.controller.get_all_centers()

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Healthcare centers retrieved successfully."
        )
        self.assertIs(result[2], expected_centers)

    def test_get_all_centers_unexpected_error(self):
        self.healthcare_center_service.get_all_centers.side_effect = (
            RuntimeError("Storage problem.")
        )

        result = self.controller.get_all_centers()

        self.assertFalse(result[0])
        self.assertEqual(
            result[1], "Could not retrieve healthcare centers."
        )
        self.assertIsNone(result[2])

    def test_update_center_success(self):
        expected_center = Mock()
        self.healthcare_center_service.update_center.return_value = (
            expected_center
        )

        result = self.controller.update_center(
            "HC001", "Updated Center", "New Street 2", "5559876"
        )

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Healthcare center updated successfully."
        )
        self.assertIs(result[2], expected_center)

    def test_update_center_error(self):
        self.healthcare_center_service.update_center.side_effect = ValueError(
            "Healthcare center not found."
        )

        result = self.controller.update_center(
            "HC999", "Updated Center", "New Street 2", "5559876"
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Healthcare center not found.")
        self.assertIsNone(result[2])

    def test_add_offering_to_center_success(self):
        expected_center = Mock()
        self.healthcare_center_service.add_offering_to_center.return_value = (
            expected_center
        )

        result = self.controller.add_offering_to_center("HC001", "O001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1],
            "Offering added to healthcare center successfully."
        )
        self.assertIs(result[2], expected_center)

        self.healthcare_center_service.add_offering_to_center.assert_called_once_with(
            "HC001", "O001"
        )

    def test_add_offering_to_center_error(self):
        self.healthcare_center_service.add_offering_to_center.side_effect = (
            ValueError("This offering is already assigned to the center.")
        )

        result = self.controller.add_offering_to_center("HC001", "O001")

        self.assertFalse(result[0])
        self.assertEqual(
            result[1], "This offering is already assigned to the center."
        )
        self.assertIsNone(result[2])

    def test_get_center_info_success(self):
        expected_info = "Center ID: HC001\nName: Wellness Center"
        self.healthcare_center_service.get_center_info.return_value = (
            expected_info
        )

        result = self.controller.get_center_info("HC001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1],
            "Healthcare center information retrieved successfully."
        )
        self.assertEqual(result[2], expected_info)

    def test_get_center_info_error(self):
        self.healthcare_center_service.get_center_info.side_effect = ValueError(
            "Healthcare center not found."
        )

        result = self.controller.get_center_info("HC999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Healthcare center not found.")
        self.assertIsNone(result[2])


if __name__ == "__main__":
    unittest.main()