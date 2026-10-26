from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from models.offering import Offering
from utils.logger import get_logger


logger = get_logger(__name__)


class OfferingService:
    def __init__(self, offering_data_access):
        self.offering_data_access = offering_data_access

    @staticmethod
    def _to_decimal(amount):
        try:
            if isinstance(amount, bool):
                raise ValueError("Price must be a valid number.")

            result = Decimal(str(amount))

            if not result.is_finite():
                raise ValueError("Price must be a finite number.")

            return result.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError("Price must be a valid monetary value.") from error

    def create_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        price = self._to_decimal(price)

        offering = Offering(
            offering_id,
            name,
            offering_type,
            price,
            duration
        )

        self.offering_data_access.add(offering)

        logger.info(
            "Offering created successfully. ID: %s",
            offering.offering_id
        )

        return offering

    def get_offering(self, offering_id):
        offering = self.offering_data_access.find_by_id(offering_id)

        if offering is None:
            logger.warning(
                "Offering not found. ID: %s",
                offering_id
            )
            raise ValueError("Offering not found.")

        return offering

    def get_all_offerings(self):
        return self.offering_data_access.get_all()

    def update_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        offering = self.get_offering(offering_id)
        price = self._to_decimal(price)

        offering.name = name
        offering.offering_type = offering_type
        offering.price = price
        offering.duration = duration

        if not self.offering_data_access.update(offering):
            logger.error(
                "Failed to update offering ID %s.",
                offering_id
            )
            raise ValueError("Failed to update offering.")

        logger.info(
            "Offering updated successfully. ID: %s",
            offering_id
        )

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