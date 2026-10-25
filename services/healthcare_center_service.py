
from models.healthcare_center import HealthcareCenter


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
        return center

    def get_center(self, center_id):
        center = self.center_data_access.find_by_id(center_id)

        if center is None:
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

        self.center_data_access.update(center)
        return center

    def get_center_info(self, center_id):
        center = self.get_center(center_id)

        return (
            f"Center ID: {center.center_id}\n"
            f"Name: {center.name}\n"
            f"Address: {center.center_address}\n"
            f"Phone: {center.center_phone_number}"
        )

    def create_offering(
        self, offering_id, name, offering_type, price, duration=None
    ):
        return self.offering_service.create_offering(
            offering_id,
            name,
            offering_type,
            price,
            duration
        )

    def get_all_offerings(self):
        return self.offering_service.get_all_offerings()

    def get_offering(self, offering_id):
        return self.offering_service.get_offering(offering_id)
