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
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_center(self, center_id):
        try:
            center = self.healthcare_center_service.get_center(center_id)

            return True, "Healthcare center found.", center

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_centers(self):
        try:
            centers = self.healthcare_center_service.get_all_centers()

            return True, "Healthcare centers retrieved successfully.", centers

        except Exception:
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
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_center_info(self, center_id):
        try:
            info = self.healthcare_center_service.get_center_info(center_id)

            return True, "Center information retrieved successfully.", info

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def create_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        try:
            offering = self.healthcare_center_service.create_offering(
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
            offering = self.healthcare_center_service.get_offering(
                offering_id
            )

            return True, "Offering found.", offering

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_offerings(self):
        try:
            offerings = self.healthcare_center_service.get_all_offerings()

            return True, "Offerings retrieved successfully.", offerings

        except Exception:
            return False, "Could not retrieve offerings.", None