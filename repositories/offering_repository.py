
from models.offering import Offering
from repositories.text_file_storage import TextFileStorage


class OfferingRepository:
    def __init__(self, storage=None):
        self.storage = storage or TextFileStorage()

    def add(self, offering):
        data = self.storage.load()
        offerings = data["offerings"]

        if any(
            item["offering_id"] == offering.offering_id
            for item in offerings
        ):
            raise ValueError("Offering ID already exists.")

        offerings.append({
            "offering_id": offering.offering_id,
            "name": offering.name,
            "offering_type": offering.offering_type,
            "price": float(offering.price),
            "duration": offering.duration
        })

        self.storage.save(data)

    def find_by_id(self, offering_id):
        data = self.storage.load()

        for item in data["offerings"]:
            if item["offering_id"] == offering_id:
                return self._to_offering(item)

        return None

    def get_all(self):
        data = self.storage.load()
        return [
            self._to_offering(item)
            for item in data["offerings"]
        ]

    def update(self, offering):
        data = self.storage.load()

        for index, item in enumerate(data["offerings"]):
            if item["offering_id"] == offering.offering_id:
                data["offerings"][index] = {
                    "offering_id": offering.offering_id,
                    "name": offering.name,
                    "offering_type": offering.offering_type,
                    "price": float(offering.price),
                    "duration": offering.duration
                }
                self.storage.save(data)
                return

        raise ValueError("Offering not found.")

    @staticmethod
    def _to_offering(item):
        return Offering(
            offering_id=item["offering_id"],
            name=item["name"],
            offering_type=item["offering_type"],
            price=float(item["price"]),
            duration=item["duration"]
        )
