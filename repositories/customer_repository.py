
from decimal import Decimal

from models.customer import Customer
from repositories.text_file_storage import TextFileStorage


class CustomerRepository:
    def __init__(self, storage=None):
        self.storage = storage or TextFileStorage()

    def add(self, customer):
        data = self.storage.load()
        customers = data.setdefault("customers", [])

        if any(
            item["customer_id"] == customer.customer_id
            for item in customers
        ):
            raise ValueError("Customer ID already exists.")

        if self.find_by_social_id(customer.social_id) is not None:
            raise ValueError("A customer with this Social ID already exists.")

        customers.append(self._to_dict(customer))
        self.storage.save(data)

    def find_by_id(self, customer_id):
        data = self.storage.load()

        for item in data.get("customers", []):
            if item["customer_id"] == customer_id:
                return self._from_dict(item)

        return None

    def find_by_social_id(self, social_id):
        data = self.storage.load()

        for item in data.get("customers", []):
            if item["social_id"] == social_id:
                return self._from_dict(item)

        return None

    def get_all(self):
        data = self.storage.load()
        return [
            self._from_dict(item)
            for item in data.get("customers", [])
        ]

    def update(self, customer):
        data = self.storage.load()
        customers = data.setdefault("customers", [])

        for index, item in enumerate(customers):
            if item["customer_id"] == customer.customer_id:
                for other in customers:
                    if (
                        other["social_id"] == customer.social_id
                        and other["customer_id"] != customer.customer_id
                    ):
                        raise ValueError(
                            "A customer with this Social ID already exists."
                        )

                customers[index] = self._to_dict(customer)
                self.storage.save(data)
                return

        raise ValueError("Customer not found.")

    @staticmethod
    def _to_dict(customer):
        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "social_id": customer.social_id,
            "age": customer.age,
            "gender": customer.gender,
            "phone_number": customer.phone_number,
            "balance": str(customer.balance)
        }

    @staticmethod
    def _from_dict(item):
        return Customer(
            customer_id=item["customer_id"],
            name=item["name"],
            social_id=item["social_id"],
            age=item["age"],
            gender=item["gender"],
            phone_number=item["phone_number"],
            balance=Decimal(item["balance"])
        )
