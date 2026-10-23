
from models.healthcare_center import HealthcareCenter


class HealthcareCenterDataAccess:
    def __init__(self, storage, offering_data_access):
        self.storage = storage
        self.offering_data_access = offering_data_access

    def add(self, center):
        data = self.storage.load()

        if self.find_by_id(center.center_id) is not None:
            raise ValueError("Center ID already exists.")

        data["centers"].append({
            "center_id": center.center_id,
            "name": center.name,
            "center_address": center.center_address,
            "center_phone_number": center.center_phone_number,
            "offering_ids": [
                offering.offering_id
                for offering in center.offerings
            ]
        })

        self.storage.save(data)

    def find_by_id(self, center_id):
        data = self.storage.load()

        for item in data["centers"]:
            if item["center_id"] == center_id:
                center = HealthcareCenter(
                    item["center_id"],
                    item["name"],
                    item["center_address"],
                    item["center_phone_number"]
                )

                for offering_id in item["offering_ids"]:
                    offering = self.offering_data_access.find_by_id(
                        offering_id
                    )

                    if offering is not None:
                        center.add_offering(offering)

                return center

        return None

    def get_all(self):
        data = self.storage.load()
        centers = []

        for item in data["centers"]:
            center = self.find_by_id(item["center_id"])
            if center is not None:
                centers.append(center)

        return centers

    def update(self, center):
        data = self.storage.load()

        for index, item in enumerate(data["centers"]):
            if item["center_id"] == center.center_id:
                data["centers"][index] = {
                    "center_id": center.center_id,
                    "name": center.name,
                    "center_address": center.center_address,
                    "center_phone_number": center.center_phone_number,
                    "offering_ids": [
                        offering.offering_id
                        for offering in center.offerings
                    ]
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, center_id):
        data = self.storage.load()

        for index, item in enumerate(data["centers"]):
            if item["center_id"] == center_id:
                del data["centers"][index]
                self.storage.save(data)
                return True

        return False
