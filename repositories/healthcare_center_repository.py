
from models.healthcare_center import HealthcareCenter
from repositories.text_file_storage import TextFileStorage


class HealthcareCenterRepository:
    def __init__(self, storage=None):
        self.storage = storage or TextFileStorage()

    def add(self, center):
        data = self.storage.load()
        centers = data.setdefault("centers", [])

        if any(
            item["center_id"] == center.center_id
            for item in centers
        ):
            raise ValueError("Center ID already exists.")

        centers.append(self._to_dict(center))
        self.storage.save(data)

    def find_by_id(self, center_id):
        data = self.storage.load()

        for item in data.get("centers", []):
            if item["center_id"] == center_id:
                return self._from_dict(item)

        return None

    def get_all(self):
        data = self.storage.load()
        return [
            self._from_dict(item)
            for item in data.get("centers", [])
        ]

    def update(self, center):
        data = self.storage.load()
        centers = data.setdefault("centers", [])

        for index, item in enumerate(centers):
            if item["center_id"] == center.center_id:
                centers[index] = self._to_dict(center)
                self.storage.save(data)
                return

        raise ValueError("Healthcare center not found.")

    @staticmethod
    def _to_dict(center):
        return {
            "center_id": center.center_id,
            "name": center.name,
            "center_address": center.center_address,
            "center_phone_number": center.center_phone_number
        }

    @staticmethod
    def _from_dict(item):
        return HealthcareCenter(
            center_id=item["center_id"],
            name=item["name"],
            center_address=item["center_address"],
            center_phone_number=item["center_phone_number"]
        )
