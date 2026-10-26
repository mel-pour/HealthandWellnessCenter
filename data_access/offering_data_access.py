from decimal import Decimal

from models.offering import Offering


class OfferingDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, offering):
        data = self.storage.load()
        offerings = data["offerings"]

        # Check for duplicate offering IDs.
        if any(
            item["offering_id"] == offering.offering_id
            for item in offerings
        ):
            raise ValueError("Offering ID already exists.")

        offerings.append({
            "offering_id": offering.offering_id,
            "name": offering.name,
            "offering_type": offering.offering_type,
            "price": str(offering.price),
            "duration": offering.duration
        })

        self.storage.save(data)
        return True

    def find_by_id(self, offering_id):
        data = self.storage.load()

        for item in data["offerings"]:
            if item["offering_id"] == offering_id:
                return self._create_offering(item)

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            self._create_offering(item)
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
                    "price": str(offering.price),
                    "duration": offering.duration
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, offering_id):
        data = self.storage.load()
        offerings = data["offerings"]

        for index, item in enumerate(offerings):
            if item["offering_id"] == offering_id:
                del offerings[index]
                self.storage.save(data)
                return True

        return False

    @staticmethod
    def _create_offering(item):
        return Offering(
            offering_id=item["offering_id"],
            name=item["name"],
            offering_type=item["offering_type"],
            price=Decimal(str(item["price"])),
            duration=item["duration"]
        )