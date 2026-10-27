import unittest
from datetime import date, time
from decimal import Decimal

from test.test_helpers import TemporaryStorageMixin
from data_access.customer_data_access import CustomerDataAccess
from data_access.offering_data_access import OfferingDataAccess
from data_access.appointment_data_access import AppointmentDataAccess
from services.customer_service import CustomerService
from services.offering_service import OfferingService
from services.appointment_service import AppointmentService


class TestAppointmentService(TemporaryStorageMixin, unittest.TestCase):
    def setUp(self):
        self.storage = self.make_storage()

        self.customer_service = CustomerService(
            CustomerDataAccess(self.storage)
        )
        self.offering_service = OfferingService(
            OfferingDataAccess(self.storage)
        )
        self.appointment_data_access = AppointmentDataAccess(self.storage)

        self.service = AppointmentService(
            self.appointment_data_access,
            self.customer_service,
            self.offering_service
        )

        self.customer_service.create_customer(
            1, "Milad", "1234567890", 30, "male",
            "09123456789", Decimal("100.00")
        )

        self.offering_service.create_offering(
            101, "Massage", "service", 50, 60
        )

    def tearDown(self):
        self.close_storage()

    def test_booking_deducts_balance_and_persists(self):
        appointment = self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        self.assertEqual(appointment.status, "booked")
        self.assertEqual(
            Decimal(str(self.customer_service.get_customer(1).balance)),
            Decimal("50.00")
        )
        self.assertEqual(
            len(self.service.get_customer_appointments(1)), 1
        )

    def test_insufficient_balance_prevents_booking(self):
        self.customer_service.deduct_balance(1, 80)

        with self.assertRaises(ValueError):
            self.service.create_appointment(
                1, 1, 101, date(2026, 11, 10), time(14, 0)
            )

        # No appointment should be saved.
        self.assertEqual(len(self.service.get_all_appointments()), 0)

    def test_cancellation_refunds_80_percent(self):
        self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        fee, refund = self.service.cancel_appointment(1)

        self.assertEqual(Decimal(str(fee)), Decimal("10.00"))
        self.assertEqual(Decimal(str(refund)), Decimal("40.00"))
        self.assertEqual(
            Decimal(str(self.customer_service.get_customer(1).balance)),
            Decimal("90.00")
        )

        self.assertEqual(
            self.service.get_appointment(1).status, "cancelled"
        )

    def test_overlapping_booking_is_rejected(self):
        self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        with self.assertRaises(ValueError):
            self.service.create_appointment(
                2, 1, 101, date(2026, 11, 10), time(14, 30)
            )

        # The rejected booking must not deduct any additional money.
        self.assertEqual(
            Decimal(str(self.customer_service.get_customer(1).balance)),
            Decimal("50.00")
        )

    def test_booking_at_end_of_existing_appointment_is_allowed(self):
        self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        appointment = self.service.create_appointment(
            2, 1, 101, date(2026, 11, 10), time(15, 0)
        )

        self.assertEqual(appointment.status, "booked")

    def test_cancelled_appointment_does_not_block_new_booking(self):
        self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        self.service.cancel_appointment(1)

        appointment = self.service.create_appointment(
            2, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        self.assertEqual(appointment.status, "booked")

    def test_cannot_cancel_appointment_twice(self):
        self.service.create_appointment(
            1, 1, 101, date(2026, 11, 10), time(14, 0)
        )

        self.service.cancel_appointment(1)

        with self.assertRaises(ValueError):
            self.service.cancel_appointment(1)

        # The customer must not receive a second refund.
        self.assertEqual(
            Decimal(str(self.customer_service.get_customer(1).balance)),
            Decimal("90.00")
        )

    def test_missing_offering_prevents_booking(self):
        with self.assertRaises(ValueError):
            self.service.create_appointment(
                1, 1, 999, date(2026, 11, 10), time(14, 0)
            )

        self.assertEqual(len(self.service.get_all_appointments()), 0)

    def test_missing_customer_prevents_booking(self):
        with self.assertRaises(ValueError):
            self.service.create_appointment(
                1, 999, 101, date(2026, 11, 10), time(14, 0)
            )

        self.assertEqual(len(self.service.get_all_appointments()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)