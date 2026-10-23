
from datetime import date, time

from models.appointment import Appointment


class AppointmentDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, appointment):
        data = self.storage.load()

        if self.find_by_id(appointment.appointment_id) is not None:
            raise ValueError("Appointment ID already exists.")

        data["appointments"].append({
            "appointment_id": appointment.appointment_id,
            "customer_id": appointment.customer_id,
            "offering_id": appointment.offering_id,
            "appointment_date": appointment.appointment_date.isoformat(),
            "start_time": appointment.start_time.isoformat(),
            "price_paid": appointment.price_paid,
            "status": appointment.status
        })

        self.storage.save(data)

    def find_by_id(self, appointment_id):
        data = self.storage.load()

        for item in data["appointments"]:
            if item["appointment_id"] == appointment_id:
                return Appointment(
                    item["appointment_id"],
                    item["customer_id"],
                    item["offering_id"],
                    date.fromisoformat(item["appointment_date"]),
                    time.fromisoformat(item["start_time"]),
                    item["price_paid"],
                    item["status"]
                )

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            Appointment(
                item["appointment_id"],
                item["customer_id"],
                item["offering_id"],
                date.fromisoformat(item["appointment_date"]),
                time.fromisoformat(item["start_time"]),
                item["price_paid"],
                item["status"]
            )
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
                    "price_paid": appointment.price_paid,
                    "status": appointment.status
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, appointment_id):
        data = self.storage.load()

        for index, item in enumerate(data["appointments"]):
            if item["appointment_id"] == appointment_id:
                del data["appointments"][index]
                self.storage.save(data)
                return True

        return False
