from datetime import date, time
from decimal import Decimal

from models.appointment import Appointment


class AppointmentDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, appointment):
        data = self.storage.load()
        appointments = data["appointments"]

        # Check for duplicate appointment ID.
        if any(
            item["appointment_id"] == appointment.appointment_id
            for item in appointments
        ):
            raise ValueError("Appointment ID already exists.")

        appointments.append({
            "appointment_id": appointment.appointment_id,
            "customer_id": appointment.customer_id,
            "offering_id": appointment.offering_id,
            "appointment_date": appointment.appointment_date.isoformat(),
            "start_time": appointment.start_time.isoformat(),
            "price_paid": str(appointment.price_paid),
            "status": appointment.status
        })

        self.storage.save(data)
        return True

    def find_by_id(self, appointment_id):
        data = self.storage.load()

        for item in data["appointments"]:
            if item["appointment_id"] == appointment_id:
                return self._create_appointment(item)

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            self._create_appointment(item)
            for item in data["appointments"]
        ]

    def update(self, appointment):
        data = self.storage.load()

        for index, item in enumerate(data["appointments"]):
            if item["appointment_id"] == appointment.appointment_id:
                data["appointments"][index] = {
                    "appointment_id": appointment.appointment_id,
                    "customer_id": appointment.customer_id,
                    "offering_id": appointment.offering_id,
                    "appointment_date": appointment.appointment_date.isoformat(),
                    "start_time": appointment.start_time.isoformat(),
                    "price_paid": str(appointment.price_paid),
                    "status": appointment.status
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, appointment_id):
        data = self.storage.load()
        appointments = data["appointments"]

        for index, item in enumerate(appointments):
            if item["appointment_id"] == appointment_id:
                del appointments[index]
                self.storage.save(data)
                return True

        return False

    @staticmethod
    def _create_appointment(item):
        return Appointment(
            appointment_id=item["appointment_id"],
            customer_id=item["customer_id"],
            offering_id=item["offering_id"],
            appointment_date=date.fromisoformat(
                item["appointment_date"]
            ),
            start_time=time.fromisoformat(
                item["start_time"]
            ),
            price_paid=Decimal(str(item["price_paid"])),
            status=item["status"]
        )
