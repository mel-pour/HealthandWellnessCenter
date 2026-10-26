from models.healthcare_center import HealthcareCenter


class HealthcareCenterDataAccess:
    def __init__(self, storage, offering_data_access):
        self.storage = storage
        self.offering_data_access = offering_data_access

    def add(self, center):
        data = self.storage.load()
        centers = data["centers"]

        # Check for duplicate center ID.
        if any(
            item["center_id"] == center.center_id
            for item in centers
        ):
            raise ValueError("Center ID already exists.")

        centers.append({
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
        return True

    def find_by_id(self, center_id):
        data = self.storage.load()

        for item in data["centers"]:
            if item["center_id"] == center_id:
                return self._create_center(item)

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            self._create_center(item)
            for item in data["centers"]
        ]

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
        centers = data["centers"]

        for index, item in enumerate(centers):
            if item["center_id"] == center_id:
                del centers[index]
                self.storage.save(data)
                return True

        return False

    def _create_center(self, item):
        offerings = []

        for offering_id in item["offering_ids"]:
            offering = self.offering_data_access.find_by_id(
                offering_id
            )

            if offering is not None:
                offerings.append(offering)

        return HealthcareCenter(
            center_id=item["center_id"],
            name=item["name"],
            center_address=item["center_address"],
            center_phone_number=item["center_phone_number"],
            offerings=offerings
        )