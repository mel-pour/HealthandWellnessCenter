class OfferingController:
    def __init__(self, offering_service):
        self.offering_service = offering_service

    def create_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        try:
            offering = self.offering_service.create_offering(
                offering_id,
                name,
                offering_type,
                price,
                duration
            )

            return True, "Offering created successfully.", offering

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_offering(self, offering_id):
        try:
            offering = self.offering_service.get_offering(offering_id)

            return True, "Offering found successfully.", offering

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_offerings(self):
        try:
            offerings = self.offering_service.get_all_offerings()

            return True, "Offerings retrieved successfully.", offerings

        except Exception:
            return False, "Could not retrieve offerings.", None

    def update_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        try:
            offering = self.offering_service.update_offering(
                offering_id,
                name,
                offering_type,
                price,
                duration
            )

            return True, "Offering updated successfully.", offering

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_offering_info(self, offering_id):
        try:
            info = self.offering_service.get_offering_info(offering_id)

            return True, "Offering information retrieved successfully.", info

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None