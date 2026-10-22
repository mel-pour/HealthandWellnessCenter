
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from models.appointment import Appointment


class AppointmentService:
    def __init__(
        self,
        appointment_repository,
        customer_service,
        offering_service
    ):
        self.appointment_repository = appointment_repository
        self.customer_service = customer_service
        self.offering_service = offering_service

    @staticmethod
    def to_decimal(amount):
        return Decimal(str(amount)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    def create_appointment(
        self,
        appointment_id,
        customer_id,
        offering_id,
        appointment_date,
        start_time
    ):
        customer = self.customer_service.get_customer(customer_id)
        offering = self.offering_service.get_offering(offering_id)

        price = self.to_decimal(offering.price)

        if not self.customer_service.has_enough_balance(
            customer_id, price
        ):
            raise ValueError("Insufficient account balance.")

        duration = offering.duration or 0
        new_start = datetime.combine(appointment_date, start_time)
        new_end = new_start + timedelta(minutes=duration)

        for existing in self.appointment_repository.get_all():
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

                if new_start < existing_end and existing_start < new_end:
                    raise ValueError(
                        "This appointment overlaps with an existing booking."
                    )

        appointment = Appointment(
            appointment_id=appointment_id,
            customer_id=customer_id,
            offering_id=offering_id,
            appointment_date=appointment_date,
            start_time=start_time,
            price_paid=float(price),
            status="booked"
        )

        # Save the appointment first. Deduct the balance only if saving works.
        self.appointment_repository.add(appointment)

        try:
            self.customer_service.deduct_balance(customer_id, price)
        except Exception:
            # Roll back the saved appointment if payment fails.
            appointment.status = "cancelled"
            self.appointment_repository.update(appointment)
            raise

        return appointment

    def get_appointment(self, appointment_id):
        appointment = self.appointment_repository.find_by_id(
            appointment_id
        )

        if appointment is None:
            raise ValueError("Appointment not found.")

        return appointment

    def get_all_appointments(self):
        return self.appointment_repository.get_all()

    def get_customer_appointments(self, customer_id):
        self.customer_service.get_customer(customer_id)
        return self.appointment_repository.get_by_customer_id(customer_id)

    def cancel_appointment(self, appointment_id):
        appointment = self.get_appointment(appointment_id)

        if appointment.status != "booked":
            raise ValueError("Only a booked appointment can be cancelled.")

        fee = self.to_decimal(appointment.price_paid * 0.20)
        refund_amount = self.to_decimal(
            appointment.price_paid
        ) - fee

        appointment.status = "cancelled"
        self.appointment_repository.update(appointment)

        self.customer_service.refund(
            appointment.customer_id,
            refund_amount
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
            f"Price: {appointment.price_paid:.2f}"
        )
