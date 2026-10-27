from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from models.appointment import Appointment
from utils.logger import get_logger


logger = get_logger(__name__)


class AppointmentService:
    def __init__(
        self,
        appointment_data_access,
        customer_service,
        offering_service
    ):
        self.appointment_data_access = appointment_data_access
        self.customer_service = customer_service
        self.offering_service = offering_service

    @staticmethod
    def to_decimal(amount):
        try:
            if isinstance(amount, bool):
                raise ValueError("Amount must be a valid number.")

            result = Decimal(str(amount))

            if not result.is_finite():
                raise ValueError("Amount must be a finite number.")

            return result.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError(
                "Amount must be a valid monetary value."
            ) from error

    def create_appointment(
        self,
        appointment_id,
        customer_id,
        offering_id,
        appointment_date,
        start_time
    ):
        # Confirm that the customer and offering exist.
        self.customer_service.get_customer(customer_id)
        offering = self.offering_service.get_offering(offering_id)

        price = self.to_decimal(offering.price)

        if price <= 0:
            raise ValueError("Offering price must be greater than zero.")

        if not self.customer_service.has_enough_balance(
            customer_id, price
        ):
            raise ValueError("Insufficient account balance.")

        # Calculate the appointment's time interval.
        duration = offering.duration or 0

        new_start = datetime.combine(appointment_date, start_time)
        new_end = new_start + timedelta(minutes=duration)

        # Prevent overlapping bookings.
        for existing in self.appointment_data_access.get_all():
            if (
                existing.status == "booked"
                and existing.appointment_date == appointment_date
            ):
                existing_offering = self.offering_service.get_offering(
                    existing.offering_id
                )

                existing_start = datetime.combine(
                    existing.appointment_date,
                    existing.start_time
                )

                existing_end = existing_start + timedelta(
                    minutes=existing_offering.duration or 0
                )

                if (
                    new_start < existing_end
                    and existing_start < new_end
                ):
                    raise ValueError(
                        "This appointment overlaps with an existing booking."
                    )

        appointment = Appointment(
            appointment_id=appointment_id,
            customer_id=customer_id,
            offering_id=offering_id,
            appointment_date=appointment_date,
            start_time=start_time,
            price_paid=price,
            status="booked"
        )

        # Save the appointment before charging the customer.
        self.appointment_data_access.add(appointment)

        try:
            self.customer_service.deduct_balance(customer_id, price)

        except Exception:
            # Attempt to cancel the appointment if payment fails.
            try:
                appointment.status = "cancelled"

                if not self.appointment_data_access.update(appointment):
                    logger.critical(
                        "Could not roll back appointment ID %s "
                        "after payment failure.",
                        appointment_id
                    )

            except Exception:
                logger.exception(
                    "Rollback failed for appointment ID %s.",
                    appointment_id
                )

            raise

        logger.info(
            "Appointment booked successfully. ID: %s",
            appointment_id
        )

        return appointment

    def get_appointment(self, appointment_id):
        appointment = self.appointment_data_access.find_by_id(
            appointment_id
        )

        if appointment is None:
            logger.warning(
                "Appointment not found. ID: %s",
                appointment_id
            )
            raise ValueError("Appointment not found.")

        return appointment

    def get_all_appointments(self):
        return self.appointment_data_access.get_all()

    def get_customer_appointments(self, customer_id):
        self.customer_service.get_customer(customer_id)

        return self.appointment_data_access.get_by_customer_id(
            customer_id
        )

    def cancel_appointment(self, appointment_id):
        appointment = self.get_appointment(appointment_id)

        if appointment.status != "booked":
            raise ValueError(
                "Only a booked appointment can be cancelled."
            )

        price = self.to_decimal(appointment.price_paid)

        fee = (price * Decimal("0.20")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        refund_amount = price - fee

        # Mark the appointment as cancelled.
        appointment.status = "cancelled"

        if not self.appointment_data_access.update(appointment):
            appointment.status = "booked"

            logger.error(
                "Failed to save cancellation for appointment ID %s.",
                appointment_id
            )

            raise ValueError("Failed to cancel appointment.")

        try:
            self.customer_service.refund(
                appointment.customer_id,
                refund_amount
            )

        except Exception:
            # Try to restore the booked status if the refund fails.
            try:
                appointment.status = "booked"

                if not self.appointment_data_access.update(appointment):
                    logger.critical(
                        "Could not restore appointment ID %s "
                        "after refund failure.",
                        appointment_id
                    )

            except Exception:
                logger.exception(
                    "Failed to restore appointment ID %s "
                    "after refund failure.",
                    appointment_id
                )

            raise

        logger.info(
            "Appointment cancelled successfully. ID: %s",
            appointment_id
        )

        return fee, refund_amount

    def get_appointment_info(self, appointment_id):
        appointment = self.get_appointment(appointment_id)

        return (
            f"Appointment ID: {appointment.appointment_id}\n"
            f"Customer ID: {appointment.customer_id}\n"
            f"Offering ID: {appointment.offering_id}\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.start_time.strftime('%H:%M')}\n"
            f"Status: {appointment.status}\n"
            f"Price: {self.to_decimal(appointment.price_paid):.2f}"
        )