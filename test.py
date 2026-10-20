
import unittest
from decimal import Decimal
from datetime import date, time

from model.customer import Customer
from model.offering import Offering
from model.appointment import Appointment
from model.health_care_center import HealthcareCenter


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.customer = Customer(
            1,
            "Milad",
            "1234567890",
            30,
            "male",
            "09123456789",
            100
        )

        self.offering = Offering(
            1, "Massage", "service", 50, 60
        )

    def test_get_info(self):
        info = self.customer.get_info()
        self.assertIn("Milad", info)
        self.assertIn("1234567890", info)

    def test_add_balance(self):
        self.customer.add_balance(25)
        self.assertEqual(self.customer.balance, Decimal("125.00"))

    def test_add_invalid_balance(self):
        with self.assertRaises(ValueError):
            self.customer.add_balance(0)

    def test_has_enough_balance(self):
        self.assertTrue(self.customer.has_enough_balance(50))
        self.assertFalse(self.customer.has_enough_balance(150))

    def test_deduct_balance(self):
        self.customer.deduct_balance(30)
        self.assertEqual(self.customer.balance, Decimal("70.00"))

    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.customer.deduct_balance(150)

    def test_refund(self):
        self.customer.refund(20)
        self.assertEqual(self.customer.balance, Decimal("120.00"))

    def test_purchase_offering(self):
        result = self.customer.purchase_offering(self.offering)
        self.assertTrue(result)
        self.assertEqual(self.customer.balance, Decimal("50.00"))

    def test_purchase_without_enough_balance(self):
        expensive_offering = Offering(
            2, "Premium Treatment", "service", 200, 60
        )
        result = self.customer.purchase_offering(expensive_offering)

        self.assertFalse(result)
        self.assertEqual(self.customer.balance, Decimal("100.00"))


class TestOffering(unittest.TestCase):

    def test_create_service(self):
        offering = Offering(1, "Massage", "service", 50, 60)

        self.assertEqual(offering.name, "Massage")
        self.assertEqual(offering.price, 50)
        self.assertEqual(offering.duration, 60)

    def test_create_facility(self):
        offering = Offering(2, "Gym Access", "facility", 15, None)

        self.assertEqual(offering.offering_type, "facility")
        self.assertIsNone(offering.duration)

    def test_get_info(self):
        offering = Offering(1, "Massage", "service", 50, 60)
        self.assertIn("Massage", offering.get_info())

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Offering(3, "Facial", "service", -10, 30)

    def test_service_without_duration(self):
        with self.assertRaises(ValueError):
            Offering(4, "Massage", "service", 50, None)


class TestHealthcareCenter(unittest.TestCase):

    def setUp(self):
        self.center = HealthcareCenter(
            1,
            "Wellness Center",
            "Main Street",
            "09123456789"
        )

        self.massage = Offering(
            1, "Massage", "service", 50, 60
        )

    def test_create_center(self):
        self.assertEqual(self.center.center_id, 1)
        self.assertEqual(self.center.name, "Wellness Center")

    def test_get_info(self):
        self.assertIn("Wellness Center", self.center.get_info())

    def test_add_offering(self):
        self.center.add_offering(self.massage)

        self.assertEqual(len(self.center.get_all_offerings()), 1)

    def test_find_offering(self):
        self.center.add_offering(self.massage)

        result = self.center.find_offering(1)

        self.assertIs(result, self.massage)

    def test_find_missing_offering(self):
        self.assertIsNone(self.center.find_offering(999))

    def test_duplicate_offering_id(self):
        self.center.add_offering(self.massage)

        duplicate = Offering(
            1, "Facial", "service", 40, 30
        )

        with self.assertRaises(ValueError):
            self.center.add_offering(duplicate)

    def test_empty_offerings(self):
        self.assertEqual(self.center.get_all_offerings(), [])


class TestAppointment(unittest.TestCase):

    def setUp(self):
        self.appointment = Appointment(
            1,
            1,
            1,
            date(2027, 5, 10),
            time(14, 0),
            100
        )

    def test_create_appointment(self):
        self.assertEqual(self.appointment.status, "pending")
        self.assertEqual(self.appointment.price_paid, 100)

    def test_get_info(self):
        info = self.appointment.get_info()
        self.assertIn("Appointment ID: 1", info)

    def test_book_appointment(self):
        self.appointment.book()
        self.assertEqual(self.appointment.status, "booked")

    def test_cannot_book_twice(self):
        self.appointment.book()

        with self.assertRaises(ValueError):
            self.appointment.book()

    def test_cancellation_fee(self):
        self.assertEqual(
            self.appointment.calculate_cancellation_fee(),
            20.0
        )

    def test_cancel_appointment(self):
        self.appointment.book()

        fee, refund = self.appointment.cancel()

        self.assertEqual(fee, 20.0)
        self.assertEqual(refund, 80.0)
        self.assertEqual(self.appointment.status, "cancelled")

    def test_cannot_cancel_pending_appointment(self):
        with self.assertRaises(ValueError):
            self.appointment.cancel()


if __name__ == "__main__":
    unittest.main(verbosity=2)
