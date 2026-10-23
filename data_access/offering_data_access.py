
from models.offering import Offering


class OfferingDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, offering):
        data = self.storage.load()

        if self.find_by_id(offering.offering_id) is not None:
            raise ValueError("Offering ID already exists.")

        data["offerings"].append({
            "offering_id": offering.offering_id,
            "name": offering.name,
            "offering_type": offering.offering_type,
            "price": offering.price,
            "duration": offering.duration
        })

        self.storage.save(data)

    def find_by_id(self, offering_id):
        data = self.storage.load()

        for item in data["offerings"]:
            if item["offering_id"] == offering_id:
                return Offering(
                    item["offering_id"],
                    item["name"],
                    item["offering_type"],
                    item["price"],
                    item["duration"]
                )

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            Offering(
                item["offering_id"],
                item["name"],
                item["offering_type"],
                item["price"],
                item["duration"]
            )
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
                    "price": offering.price,
                    "duration": offering.duration
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, offering_id):
        data = self.storage.load()

        for index, item in enumerate(data["offerings"]):
            if item["offering_id"] == offering_id:
                del data["offerings"][index]
                self.storage.save(data)
                return True

        return False
