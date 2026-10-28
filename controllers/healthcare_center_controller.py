from utils.logger import get_logger

logger = get_logger(__name__)


class HealthcareCenterController:

    def __init__(self, healthcare_center_service):
        self.healthcare_center_service = healthcare_center_service

    def create_center(
        self, center_id, name, center_address, center_phone_number
    ):
        try:
            center = self.healthcare_center_service.create_center(
                center_id,
                name,
                center_address,
                center_phone_number
            )

            return True, "Healthcare center created successfully.", center

        except (ValueError, TypeError) as error:
            logger.warning("Could not create healthcare center: %s", error)
            return False, str(error), None

        except Exception:
            logger.exception("Unexpected error while creating healthcare center.")
            return False, "An unexpected error occurred.", None

    def get_center(self, center_id):
        try:
            center = self.healthcare_center_service.get_center(center_id)

            return True, "Healthcare center found successfully.", center

        except (ValueError, TypeError) as error:
            logger.warning("Could not retrieve healthcare center: %s", error)
            return False, str(error), None

        except Exception:
            logger.exception("Unexpected error while retrieving healthcare center.")
            return False, "An unexpected error occurred.", None

    def get_all_centers(self):
        try:
            centers = self.healthcare_center_service.get_all_centers()

            return True, "Healthcare centers retrieved successfully.", centers

        except Exception:
            logger.exception("Could not retrieve healthcare centers.")
            return False, "Could not retrieve healthcare centers.", None

    def update_center(
        self, center_id, name, center_address, center_phone_number
    ):
        try:
            center = self.healthcare_center_service.update_center(
                center_id,
                name,
                center_address,
                center_phone_number
            )

            return True, "Healthcare center updated successfully.", center

        except (ValueError, TypeError) as error:
            logger.warning("Could not update healthcare center: %s", error)
            return False, str(error), None

        except Exception:
            logger.exception("Unexpected error while updating healthcare center.")
            return False, "An unexpected error occurred.", None

    def add_offering_to_center(self, center_id, offering_id):
        try:
            center = self.healthcare_center_service.add_offering_to_center(
                center_id,
                offering_id
            )

            return (
                True,
                "Offering added to healthcare center successfully.",
                center
            )

        except (ValueError, TypeError) as error:
            logger.warning("Could not add offering to healthcare center: %s", error)
            return False, str(error), None

        except Exception:
            logger.exception("Unexpected error while adding offering to healthcare center.")
            return False, "An unexpected error occurred.", None

    def get_center_info(self, center_id):
        try:
            info = self.healthcare_center_service.get_center_info(center_id)

            return (
                True,
                "Healthcare center information retrieved successfully.",
                info
            )

        except (ValueError, TypeError) as error:
            logger.warning("Could not retrieve healthcare center information: %s", error)
            return False, str(error), None

        except Exception:
            logger.exception("Unexpected error while retrieving healthcare center information.")
            return False, "An unexpected error occurred.", None