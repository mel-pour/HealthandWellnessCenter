
from decimal import Decimal, ROUND_HALF_UP
from models.offering import Offering


class OfferingService:
    def __init__(self, offering_repository):
        self.offering_repository = offering_repository

    def create_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        offering = Offering(
            offering_id, name, offering_type, price, duration
        )
        self.offering_repository.add(offering)
        return offering

    def get_offering(self, offering_id):
        offering = self.offering_repository.find_by_id(offering_id)

        if offering is None:
            raise ValueError("Offering not found.")

        return offering

    def get_all_offerings(self):
        return self.offering_repository.get_all()

    def update_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        offering = self.get_offering(offering_id)

        offering.name = name
        offering.offering_type = offering_type
        offering.price = Decimal(str(price)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        offering.duration = duration

        self.offering_repository.update(offering)
        return offering

    def get_offering_info(self, offering_id):
        offering = self.get_offering(offering_id)

        duration_text = (
            str(offering.duration)
            if offering.duration is not None
            else "Not applicable"
        )

        return (
            f"ID: {offering.offering_id}\n"
            f"Name: {offering.name}\n"
            f"Type: {offering.offering_type}\n"
            f"Price: {offering.price}\n"
            f"Duration: {duration_text}"
        )
