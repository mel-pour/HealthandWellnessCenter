from models.healthcare_center import HealthcareCenter
from utils.logger import get_logger


logger = get_logger(__name__)


class HealthcareCenterService:
    def __init__(self, center_data_access, offering_service):
        self.center_data_access = center_data_access
        self.offering_service = offering_service

    def create_center(
        self, center_id, name, center_address, center_phone_number
    ):
        center = HealthcareCenter(
            center_id,
            name,
            center_address,
            center_phone_number
        )

        self.center_data_access.add(center)

        logger.info(
            "Healthcare center created successfully. ID: %s",
            center_id
        )

        return center

    def get_center(self, center_id):
        center = self.center_data_access.find_by_id(center_id)

        if center is None:
            logger.warning(
                "Healthcare center not found. ID: %s",
                center_id
            )
            raise ValueError("Healthcare center not found.")

        return center

    def get_all_centers(self):
        return self.center_data_access.get_all()

    def update_center(
        self, center_id, name, center_address, center_phone_number
    ):
        center = self.get_center(center_id)

        center.name = name
        center.center_address = center_address
        center.center_phone_number = center_phone_number

        if not self.center_data_access.update(center):
            logger.error(
                "Failed to update healthcare center ID %s.",
                center_id
            )
            raise ValueError("Failed to update healthcare center.")

        logger.info(
            "Healthcare center updated successfully. ID: %s",
            center_id
        )

        return center

    def add_offering_to_center(self, center_id, offering_id):
        center = self.get_center(center_id)
        offering = self.offering_service.get_offering(offering_id)

        # Prevent the same offering from being added twice.
        if any(
            existing.offering_id == offering_id
            for existing in center.offerings
        ):
            raise ValueError(
                "This offering is already assigned to the center."
            )

        center.offerings.append(offering)

        if not self.center_data_access.update(center):
            # Restore the in-memory object if persistence fails.
            center.offerings.remove(offering)

            logger.error(
                "Failed to add offering ID %s to center ID %s.",
                offering_id,
                center_id
            )

            raise ValueError("Failed to add offering to healthcare center.")

        logger.info(
            "Offering ID %s added to healthcare center ID %s.",
            offering_id,
            center_id
        )

        return center

    def get_center_info(self, center_id):
        center = self.get_center(center_id)

        return (
            f"Center ID: {center.center_id}\n"
            f"Name: {center.name}\n"
            f"Address: {center.center_address}\n"
            f"Phone: {center.center_phone_number}"
        )