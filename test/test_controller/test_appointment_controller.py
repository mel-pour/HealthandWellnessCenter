import unittest
from unittest.mock import Mock

from controllers.appointment_controller import AppointmentController


class TestAppointmentController(unittest.TestCase):

    def setUp(self):
        self.appointment_service = Mock()
        self.controller = AppointmentController(self.appointment_service)

    def test_create_appointment_success(self):
        expected_appointment = Mock()
        self.appointment_service.create_appointment.return_value = (
            expected_appointment
        )

        result = self.controller.create_appointment(
            "A001", "C001", "O001", "2026-11-01", "10:00"
        )

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Appointment booked successfully.")
        self.assertIs(result[2], expected_appointment)

        self.appointment_service.create_appointment.assert_called_once_with(
            "A001", "C001", "O001", "2026-11-01", "10:00"
        )

    def test_create_appointment_validation_error(self):
        self.appointment_service.create_appointment.side_effect = ValueError(
            "Insufficient account balance."
        )

        result = self.controller.create_appointment(
            "A001", "C001", "O001", "2026-11-01", "10:00"
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Insufficient account balance.")
        self.assertIsNone(result[2])

    def test_create_appointment_unexpected_error(self):
        self.appointment_service.create_appointment.side_effect = RuntimeError(
            "Unexpected problem."
        )

        result = self.controller.create_appointment(
            "A001", "C001", "O001", "2026-11-01", "10:00"
        )

        self.assertFalse(result[0])
        self.assertEqual(result[1], "An unexpected error occurred.")
        self.assertIsNone(result[2])

    def test_get_appointment_success(self):
        expected_appointment = Mock()
        self.appointment_service.get_appointment.return_value = (
            expected_appointment
        )

        result = self.controller.get_appointment("A001")

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Appointment found successfully.")
        self.assertIs(result[2], expected_appointment)

    def test_get_appointment_not_found(self):
        self.appointment_service.get_appointment.side_effect = ValueError(
            "Appointment not found."
        )

        result = self.controller.get_appointment("A999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Appointment not found.")
        self.assertIsNone(result[2])

    def test_get_all_appointments_success(self):
        expected_appointments = [Mock(), Mock()]
        self.appointment_service.get_all_appointments.return_value = (
            expected_appointments
        )

        result = self.controller.get_all_appointments()

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Appointments retrieved successfully."
        )
        self.assertIs(result[2], expected_appointments)

    def test_get_all_appointments_unexpected_error(self):
        self.appointment_service.get_all_appointments.side_effect = (
            RuntimeError("Storage problem.")
        )

        result = self.controller.get_all_appointments()

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Could not retrieve appointments.")
        self.assertIsNone(result[2])

    def test_get_customer_appointments_success(self):
        expected_appointments = [Mock()]
        self.appointment_service.get_customer_appointments.return_value = (
            expected_appointments
        )

        result = self.controller.get_customer_appointments("C001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Customer appointments retrieved successfully."
        )
        self.assertIs(result[2], expected_appointments)

        self.appointment_service.get_customer_appointments.assert_called_once_with(
            "C001"
        )

    def test_get_customer_appointments_error(self):
        self.appointment_service.get_customer_appointments.side_effect = (
            ValueError("Customer not found.")
        )

        result = self.controller.get_customer_appointments("C999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Customer not found.")
        self.assertIsNone(result[2])

    def test_cancel_appointment_success(self):
        self.appointment_service.cancel_appointment.return_value = (
            10, 40
        )

        result = self.controller.cancel_appointment("A001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Appointment cancelled successfully."
        )
        self.assertEqual(
            result[2],
            {
                "cancellation_fee": 10,
                "refund_amount": 40
            }
        )

        self.appointment_service.cancel_appointment.assert_called_once_with(
            "A001"
        )

    def test_cancel_appointment_error(self):
        self.appointment_service.cancel_appointment.side_effect = ValueError(
            "Appointment already cancelled."
        )

        result = self.controller.cancel_appointment("A001")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Appointment already cancelled.")
        self.assertIsNone(result[2])

    def test_get_appointment_info_success(self):
        expected_info = "Appointment ID: A001"
        self.appointment_service.get_appointment_info.return_value = (
            expected_info
        )

        result = self.controller.get_appointment_info("A001")

        self.assertTrue(result[0])
        self.assertEqual(
            result[1], "Appointment information retrieved successfully."
        )
        self.assertEqual(result[2], expected_info)

    def test_get_appointment_info_error(self):
        self.appointment_service.get_appointment_info.side_effect = ValueError(
            "Appointment not found."
        )

        result = self.controller.get_appointment_info("A999")

        self.assertFalse(result[0])
        self.assertEqual(result[1], "Appointment not found.")
        self.assertIsNone(result[2])


if __name__ == "__main__":
    unittest.main()