
from datetime import date, time

from models.appointment import Appointment
from repositories.text_file_storage import TextFileStorage


class AppointmentRepository:
    def __init__(self, storage=None):
        self.storage = storage or TextFileStorage()

    def add(self, appointment):
        data = self.storage.load()
        appointments = data.setdefault("appointments", [])

        if any(
            item["appointment_id"] == appointment.appointment_id
            for item in appointments
        ):
            raise ValueError("Appointment ID already exists.")

        appointments.append(self._to_dict(appointment))
        self.storage.save(data)

    def find_by_id(self, appointment_id):
        data = self.storage.load()

        for item in data.get("appointments", []):
            if item["appointment_id"] == appointment_id:
                return self._from_dict(item)

        return None

    def get_all(self):
        data = self.storage.load()
        return [
            self._from_dict(item)
            for item in data.get("appointments", [])
        ]

    def get_by_customer_id(self, customer_id):
        return [
            appointment
            for appointment in self.get_all()
            if appointment.customer_id == customer_id
        ]

    def update(self, appointment):
        data = self.storage.load()
        appointments = data.setdefault("appointments", [])

        for index, item in enumerate(appointments):
            if item["appointment_id"] == appointment.appointment_id:
                appointments[index] = self._to_dict(appointment)
                self.storage.save(data)
                return

        raise ValueError("Appointment not found.")

    @staticmethod
    def _to_dict(appointment):
        return {
            "appointment_id": appointment.appointment_id,
            "customer_id": appointment.customer_id,
            "offering_id": appointment.offering_id,
            "appointment_date": appointment.appointment_date.isoformat(),
            "start_time": appointment.start_time.isoformat(),
            "price_paid": float(appointment.price_paid),
            "status": appointment.status
        }

    @staticmethod
    def _from_dict(item):
        return Appointment(
            appointment_id=item["appointment_id"],
            customer_id=item["customer_id"],
            offering_id=item["offering_id"],
            appointment_date=date.fromisoformat(
                item["appointment_date"]
            ),
            start_time=time.fromisoformat(item["start_time"]),
            price_paid=float(item["price_paid"]),
            status=item["status"]
        )
